# Technical Context

## Architecture
- **Cog-based structure** for modular command organization
- **Global database instance** (`db`) from `database.py`
- **Dual storage**: Supabase primary, JSON fallback on failure
- **Comprehensive logging**: Python logging module for all database operations

## Database Schema (Supabase)

### Tables
1. **reaction_roles**: Maps message IDs to reaction role data
   - `message_id` TEXT PRIMARY KEY
   - `data` JSONB (contains type, channel_id, guild_id, roles mapping)

2. **warnings**: Tracks user warnings per guild
   - `guild_id`, `user_id` composite unique key
   - `warnings` JSONB array

3. **suggestions**: Stores wish/suggestion data
   - `message_id` TEXT PRIMARY KEY
   - `data` JSONB (type, author_id, description, guild_id, votes, created_at)
   - **NOTE**: Currently missing `channel_id` in JSONB data - needed for linking

## Cogs
- `suggestions.py`: Wish system, voting, weekly summary
- `roles.py`: Role setup, reaction role creation
- `moderation.py`: Kick, ban, warn, timeout commands
- `utilities.py`: Misc commands (ping, whisper, etc.)

## Key Patterns
- **Embed-based messaging**: All bot responses use Discord embeds with Ahamkara theming
- **Permission checks**: `has_mod_role()` decorator, `has_dreamer_role()` method
- **Cooldowns**: Help command has 5-minute cooldown
- **Weekly tasks**: Loop runs every Monday at midnight UTC
- **Vote threshold**: Channel suggestions auto-create when reaching 67% of server members

## Data Flow
1. User makes wish → Message posted with reaction
2. Reactions tracked → Vote count updated in database
3. Channel wishes → Auto-create if threshold met
4. Weekly task → Summarizes top suggestions

## Constants (config/constants.py)
- Role definitions (MOD_ROLES, DREAMER_ROLE, COLOR_ROLES, EXOTIC_COLORS, SPECIAL_ROLES)
- Whisper phrases (ELDRITCH_WHISPERS)
- Activity phrases (AHAMKARA_ACTIVITIES)

## Database Logging (Session 5)

### Logging Strategy
All database operations in `src/database.py` use Python's `logging` module for comprehensive error tracking and debugging.

### Log Levels
- **INFO**: Successful operations, includes item counts
  - `[Database] load_suggestions: Success (23 items from Supabase)`
  - `[Database] save_warnings: Success (5 users to JSON)`
- **WARNING**: Fallback to JSON when Supabase fails
  - `[Database] save_suggestions: Supabase error, falling back to JSON: [ConnectionError] timeout`
  - `[Database] Initialized with Supabase connection`
- **ERROR**: Complete failures (both Supabase and JSON)
  - `[Database] load_warnings: JSON read failed: [JSONDecodeError] ...`
  - `[Database] increment_whisper_usage: Failed for 'whisper_001': ...`
- **DEBUG**: Detailed operation tracking
  - `[Database] increment_8ball_usage: New response '8ball_001'`
  - `[Database] increment_8ball_usage: '8ball_001' now at 5 uses`

### Error Handling Pattern
All database methods follow this pattern:
1. Attempt primary operation (Supabase or JSON based on config)
2. Log success with context (operation name, item count)
3. On error: Log exception type and message
4. Fallback to JSON if Supabase fails
5. Return safe defaults (empty dict, fallback count) on total failure

### Production Benefits
- **Debugging**: Detailed error context (operation, data type, exception)
- **Monitoring**: Track fallback usage (Supabase reliability)
- **Diagnostics**: Identify patterns in failures
- **No breaking changes**: Preserves existing dual-storage behavior
