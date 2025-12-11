# Dreambot Status

**Last Updated**: 2025-12-11 (Session 13)
**Session**: Rate Limit Handling & Deployment Fix

## Current State

### Session 13: Rate Limit Handling
- **Root cause identified**: Cloudflare-level 429 blocking during Render deployments
- **Multiple instances**: Render spins up new instances while old ones run, causing concurrent gateway connections
- **Solution implemented**: Exponential backoff with jitter for bot startup
- **Bulk operation delays**: Added rate limit delays to reaction-heavy operations

### Changes Made
- `src/main.py`: Complete rewrite with `start_bot_with_backoff()`
  - Exponential backoff: 30s base, doubles each retry, max 15 minutes
  - Jitter: ±50% to prevent thundering herd
  - Respects Discord's Retry-After header when available
  - 10 retry attempts before giving up
- `src/cogs/roles.py`: Added 300ms delays between adding reactions
- `src/cogs/suggestions.py`: Added 100ms delays between message fetches

### Previous Sessions

**Session 12: Code Organization & Testing Tools**
- !help moved: Suggestions -> Utilities cog
- Schema updated: 25 new tables for intent pool usage
- Chat tester: `tools/chat_tester.py` for offline response testing

**Conversational Enhancement System (Sessions 10-11)**
- Intent Detection: 21 priority-based intents, 50.7% coverage
- Topic Extraction: ELIZA-style `{topic}` substitution
- Context Memory: Per-user history, running jokes, repetition detection, lore callbacks
- Escape Paths: Auto-disengage from spammy users (6 msgs/2min threshold)
- Response Pools: 25 pools, ~220 total responses
- All 95 tests passing

### Core Features
- Wish management system (active/granted lifecycle)
- Reaction count synchronization (persists across restarts)
- Interactive tag responses (magic 8-ball + vague statements)
- Weighted response selection (1/(usage+1)^2 algorithm)
- ID-based architecture (edit responses without losing stats)
- Universal zalgo transformation
- Comprehensive database error logging
- **Security**: A- rating, zero critical vulnerabilities

## Deployment Status

### The Problem
When deploying on Render:
1. New instance starts while old instance is still connected
2. Both try to authenticate with Discord simultaneously
3. Discord's Cloudflare protection issues IP-level 429
4. Bot crashes and retries immediately, making it worse

### The Solution
```python
# Exponential backoff pattern
delay = min(BASE_DELAY * (2 ** retry_count), MAX_DELAY)
jitter = delay * random.uniform(-0.5, 0.5)
await asyncio.sleep(delay + jitter)
```

Delays:
- Attempt 1: ~30s (15-45s with jitter)
- Attempt 2: ~60s
- Attempt 3: ~120s
- Attempt 4: ~240s
- Attempt 5: ~480s
- Attempts 6+: ~900s (15 minute cap)

## Next Steps

1. **Deploy** - Commit and push changes
2. **Monitor** - Watch Render logs for successful connection
3. **Verify** - Ensure bot comes online after rate limit clears

## Command Reference

**Interactive Features:**
- Tag @Dreambot -> Intent-detected response from appropriate pool
- Questions -> 8-ball pool (35 responses) or intent-specific
- Statements -> Vague pool (29 responses) or intent-specific
- Kebab 3+ times -> Escalating intense responses
- Ask same thing twice -> Repetition acknowledgment
- Mention lore -> 5% chance of vortex callback

**Admin Commands:**
- `!harvest [channel] [limit]` - Collect conversation data
- `!manifestwish <id> [notes]` - Mark wish granted
- `!removewish <id>` - Delete wish
- `!weeklysummary` - Manual summary trigger
- `!speak <message>` - Post to #general-chat

**Public Commands:**
- `!wish <type> <description>` - Create wish
- `!topvideos [limit]` - View top video wishes
- `!topother [limit]` - View top other wishes
- `!manifestations [type] [limit]` - View granted wishes
