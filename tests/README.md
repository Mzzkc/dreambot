# Dreambot Unit Tests

## Overview
Unit tests for the dreambot Discord bot, focusing on the suggestion system's reaction synchronization functionality.

## Test Coverage

### `test_suggestions_sync.py`
Comprehensive tests for the `sync_reaction_counts()` method which reconciles database vote counts with actual Discord message reactions.

**Test Cases:**
1. ✅ `test_sync_updates_stale_counts` - Verifies sync updates out-of-date vote counts
2. ✅ `test_sync_removes_deleted_messages` - Confirms deleted messages are removed from DB
3. ✅ `test_sync_handles_missing_channels` - Validates graceful handling of missing channels
4. ✅ `test_sync_handles_permission_errors` - Tests error handling for permission issues
5. ✅ `test_sync_auto_manifests_channel_at_threshold` - Confirms auto-creation of channels at threshold
6. ✅ `test_sync_does_not_manifest_below_threshold` - Validates channels NOT created below threshold
7. ✅ `test_sync_ignores_granted_wishes` - Ensures granted wishes are skipped
8. ✅ `test_sync_multiple_wishes_mixed_scenarios` - Tests handling of multiple concurrent scenarios
9. ✅ `test_sync_returns_empty_stats_for_no_suggestions_channel` - Validates empty stats when channel missing
10. ✅ `test_sync_filters_by_guild` - Confirms only specified guild's wishes are processed

**All 10 tests passing as of 2025-11-21**

## Running Tests

### Option 1: Use the test runner script
```bash
./run_tests.sh
```

### Option 2: Direct pytest invocation
```bash
# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH and run tests
export PYTHONPATH=/home/emzi/Projects/dreambot/src
pytest tests/ -v
```

### Option 3: Run specific test file
```bash
source venv/bin/activate
export PYTHONPATH=/home/emzi/Projects/dreambot/src
pytest tests/test_suggestions_sync.py -v
```

### Option 4: Run specific test
```bash
source venv/bin/activate
export PYTHONPATH=/home/emzi/Projects/dreambot/src
pytest tests/test_suggestions_sync.py::test_sync_updates_stale_counts -v
```

## Dependencies

Test dependencies are listed in `requirements-dev.txt`:
- `pytest==7.4.3` - Test framework
- `pytest-asyncio==0.21.1` - Async test support
- `pytest-mock==3.12.0` - Mocking utilities

Install with:
```bash
pip install -r requirements-dev.txt
```

## Test Configuration

Tests are configured via `pytest.ini`:
- Test discovery pattern: `test_*.py`
- Async mode: Auto
- Test path: `tests/`

## Architecture

Tests use comprehensive mocking to isolate the sync logic:
- **Discord objects**: Mock Guild, TextChannel, Message, Reaction
- **Database operations**: Mock load/save methods
- **Bot instance**: Mock Discord bot with test data

This approach allows testing sync logic without requiring:
- Live Discord connection
- Actual database instance
- Running bot process

## Maintenance

When modifying `src/cogs/suggestions.py`:
1. Run tests to ensure no regressions
2. Add new tests for new functionality
3. Update this README if test coverage changes

## Continuous Integration

These tests are suitable for CI/CD pipelines:
- Fast execution (< 1 second)
- No external dependencies
- Deterministic results
- Clear pass/fail outcomes
