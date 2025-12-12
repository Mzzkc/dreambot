# Active Context

## Session 15 - Weighting Investigation

**Last Updated:** 2025-12-12
**Status:** COMPLETE - Investigation resolved, diagnostic logging added (`05239aa`)

### What Was Done

**Issue:** User reported same responses appearing multiple times in a row, suspected weighting wasn't working.

**Investigation (TDF-aligned):**
1. Traced code paths - all response selection uses weighted `random.choices`
2. Verified algorithm: `weight = 1/(usage+1)²` is correct
3. Checked Supabase tables - all intent pool tables exist
4. Analyzed logs - earlier "0 items" were first-time pool usage
5. Confirmed data persists - `greeting` table has data, loads correctly now

**Key Finding:** Logs from 14:18:57 show `load_pool_usage(greeting): Success (1 items from Supabase)` - weighting IS working. The vague_016 at 9 vs others at 4-7 is normal statistical variance for the algorithm.

**Changes:**
- Added diagnostic logging in `database.py` for pool usage persistence
- Warnings when tables return empty or upserts fail silently

**Commit:** `05239aa` - pushed to main

### Next Steps

Phase 4 refinements (optional, if repetition still feels frequent):
- More aggressive weighting curves
- Per-user vs global weighting
- Decay over time
- Pool-specific tuning

---

## Previous Sessions

- **Session 14**: {topic} bug fix (`0ecfb0e`)
- **Session 13**: Rate limit handling, slumber mode (`a5ae42f`)
- **Session 12**: Code organization, chat tester tool
- **Session 11**: Escape paths for spammy users
- **Session 10**: Conversational enhancement (21 intents, topic extraction)
- **Session 9**: Conversation harvester
- **Session 8**: Reaction sync, unit tests
- **Session 7**: Security audit (A- rating)
