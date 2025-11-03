# Supabase Database Setup

This document contains the SQL commands needed to set up the database tables for Dreambot.

## Required Tables

### 1. Reaction Roles Table

```sql
CREATE TABLE reaction_roles (
    id SERIAL PRIMARY KEY,
    message_id TEXT NOT NULL UNIQUE,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Warnings Table

```sql
CREATE TABLE warnings (
    id SERIAL PRIMARY KEY,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    warnings JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(guild_id, user_id)
);
```

### 3. Suggestions Table

```sql
CREATE TABLE suggestions (
    id SERIAL PRIMARY KEY,
    message_id TEXT NOT NULL UNIQUE,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Sample Data Structure

### Suggestions Data Structure

The `data` JSONB field in the suggestions table contains:

```json
{
    "type": "video|channel|other",
    "author_id": 123456789012345678,
    "description": "Description of the suggestion",
    "guild_id": 987654321098765432,
    "channel_id": 123456789012345678,
    "votes": 5,
    "created_at": "2023-01-01T00:00:00Z"
}
```

**Note:** The `channel_id` field was added in a recent update to support message links in the weekly summary. For existing suggestions, run the `!migratewishes` command as a moderator to backfill this data.

### Reaction Roles Data Structure

The `data` JSONB field in the reaction_roles table contains:

```json
{
    "channel_id": 123456789012345678,
    "guild_id": 987654321098765432,
    "roles": {
        "🔴": "Role Name 1",
        "🟦": "Role Name 2"
    }
}
```

### Warnings Data Structure

The `warnings` JSONB field contains an array of warning objects:

```json
[
    {
        "reason": "Violation of rule 1",
        "moderator": "Moderator#1234",
        "timestamp": "2023-01-01T00:00:00Z"
    }
]
```

## Environment Variables

Make sure to set these environment variables:

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service key (not the anon key)
- `DISCORD_TOKEN`: Your Discord bot token

## Permissions

Ensure your Supabase service key has the following permissions:
- INSERT on all tables
- SELECT on all tables
- UPDATE on all tables
- DELETE on all tables

## Fallback

If Supabase is not configured or fails, the bot will automatically fall back to using JSON files:
- `reaction_roles.json`
- `warnings.json`
- `suggestions.json`

## Migration Instructions

### Upgrading from Previous Versions

If you're upgrading from a version before the `channel_id` addition:

1. **No Supabase changes needed** - The JSONB schema is flexible
2. **After deploying the updated bot**, run this command in Discord as a moderator:
   ```
   !migratewishes
   ```
3. This will backfill the `channel_id` field for all existing suggestions
4. The weekly summary will now include clickable links to original suggestion posts

### New Features in This Update

**Admin Commands:**
- `!removewish <message_id>` - Remove a suggestion from the database
- `!migratewishes` - Backfill channel_id for existing suggestions (one-time use)

**Weekly Summary Enhancement:**
- Now includes clickable links to view the original suggestion posts
- Shows more context per suggestion (80 characters vs 50)

**Pronoun Roles:**
- New pronoun section in role setup with 13 pronoun options
- Includes standard pronouns (he/him, she/her, they/them, etc.)
- Includes neo pronouns (xe/xem, ze/zir, fae/faer, e/em, ve/ver)
- Users can select multiple pronoun roles