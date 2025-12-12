# Dreambot Status

**Last Updated**: 2025-12-12 (Session 15)
**Deploy Status**: Live on Render

## Current State

### Session 15: Weighting Investigation ✅

**Investigation:** User reported repeated responses - suspected weighting not working

**Findings:**
- Weighting algorithm (1/(usage+1)²) is correct and functional
- Intent pool tables exist in Supabase and persist data correctly
- Earlier "0 items" logs were first-time pool usage (expected)
- Subsequent loads show correct item counts (e.g., `greeting: 1 items`)
- vague_016 at 9 vs others at 4-7 is normal statistical variance

**Changes:**
- Added diagnostic logging for pool usage persistence (`05239aa`)
- Warnings when tables return empty or upserts fail silently

**Commit:** `05239aa` pushed to main

### Session 14: {topic} Bug Fix ✅

**Problem:** Literal `{topic}` appearing in responses when topic extraction failed

**Solution:**
- Exclude `{topic}` templates when no topic available
- Keyword fallback for topic extraction (META_LORE, EXISTENTIAL intents)

**Commit:** `0ecfb0e` pushed to main

### Core Features
- Wish management (active/granted lifecycle)
- Reaction count sync (persists across restarts)
- Conversational system (21 intents, topic extraction, context memory)
- Weighted response selection (1/(usage+1)^2)
- Escape paths (auto-disengage spammy users)
- Security: A- rating

## Rate Limit Configuration

```python
# Startup (main.py)
MAX_RETRIES = 10
BASE_DELAY = 30s, MAX_DELAY = 900s (15min)
SLUMBER_DURATION = 2 hours
MAX_SLUMBER_CYCLES = 12 (24hr total)

# Operations
ROLE_CREATE_DELAY = 500ms
REACTION_DELAY = 300ms
MESSAGE_FETCH_DELAY = 100ms
HARVEST_BATCH_DELAY = 500ms (100 msgs/batch)
ROLE_MODIFY_DELAY = 250ms
```

## Next Steps

1. **Phase 4 refinements** (if repetition still feels frequent):
   - More aggressive weighting curves
   - Per-user vs global weighting
   - Decay over time for old usage counts
   - Pool-specific tuning for smaller pools

## Command Reference

**Interactive:** @Dreambot → intent-detected responses
**Admin:** !harvest, !manifestwish, !removewish, !weeklysummary, !speak
**Public:** !wish, !topvideos, !topother, !manifestations
