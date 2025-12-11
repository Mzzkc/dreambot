# Active Context

## Session 13 - Rate Limit Handling & Deployment Fix

**Last Updated:** 2025-12-11

### The Problem

Render deployments were failing with HTTP 429 (Too Many Requests) from Discord's Cloudflare protection:

```
discord.errors.HTTPException: 429 Too Many Requests (error code: 0): <!DOCTYPE html>
```

**Root Cause Analysis:**
1. Render spins up new instances during zero-downtime deployments
2. Multiple instances (old + new) try to connect to Discord gateway simultaneously
3. Discord's Cloudflare layer sees rapid requests from same IP/token
4. Cloudflare issues IP-level 429 (not per-endpoint rate limit)
5. Bot crashes and retries immediately, compounding the problem

**Evidence from logs:**
- Multiple instance IDs hitting 429 simultaneously (`srv-...-xnhlv`, `srv-...-qf75q`, etc.)
- HTML response is Cloudflare error page, not Discord API JSON
- `error code: 0` indicates pre-API blocking

### The Solution

**1. Exponential Backoff at Startup (`src/main.py`)**

```python
# Configuration
MAX_RETRIES = 10
BASE_DELAY = 30  # Start with 30 second delay
MAX_DELAY = 900  # Cap at 15 minutes
JITTER_RANGE = 0.5  # ±50% jitter

# Pattern
delay = min(BASE_DELAY * (2 ** retry_count), MAX_DELAY)
jitter = delay * random.uniform(-JITTER_RANGE, JITTER_RANGE)
await asyncio.sleep(delay + jitter)
```

**Delay progression:**
- Attempt 1: ~30s (15-45s with jitter)
- Attempt 2: ~60s (30-90s)
- Attempt 3: ~120s (60-180s)
- Attempt 4: ~240s (120-360s)
- Attempt 5: ~480s (240-720s)
- Attempt 6+: ~900s (450-1350s, capped at 15 min)

**2. Rate Limit Delays in Bulk Operations**

- `src/cogs/roles.py`: 300ms delay between adding reactions in `setup_roles`
- `src/cogs/suggestions.py`: 100ms delay between message fetches in `sync_reaction_counts`

### Files Modified

```
src/main.py              # Complete rewrite with backoff
src/cogs/roles.py        # Added REACTION_DELAY (300ms)
src/cogs/suggestions.py  # Added MESSAGE_FETCH_DELAY (100ms)
```

### Key Insights

**Why discord.py's built-in rate limiting didn't help:**
- discord.py handles per-endpoint rate limits (429 with JSON body)
- Cloudflare-level blocks return HTML, not JSON
- These are IP-level blocks, not API route limits
- The library doesn't catch and retry these gracefully

**Why jitter matters:**
- Multiple Render instances might retry at exactly the same intervals
- Without jitter, retries stay synchronized and keep hitting limits
- ±50% randomization desynchronizes retry attempts

### Test Results

All 95 tests pass:
```
tests/test_escape_detection.py: 20 passed
tests/test_intent_detection.py: 65 passed
tests/test_suggestions_sync.py: 10 passed
```

### Next Steps

1. Commit and push changes
2. Trigger Render deployment
3. Monitor logs for backoff behavior
4. Verify bot connects successfully after rate limit clears

---

## Previous Sessions Summary

- **Session 12**: Code organization (!help moved), schema updates, chat tester tool
- **Session 11**: Escape paths (auto-disengage from spammy users), intent fixes
- **Session 10**: Conversational enhancement (21 intents, topic extraction, context)
- **Session 9**: Conversation harvester (`!harvest`) for training data
- **Session 8**: Reaction sync implementation, unit test suite
- **Session 7**: Security audit (A- rating, safe for production)
