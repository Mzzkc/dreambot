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
    "votes": 5,
    "created_at": "2023-01-01T00:00:00Z"
}
```

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