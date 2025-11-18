-- DreamBot Database Schema
-- Run these commands in your Supabase SQL editor to create the required tables

-- Reaction roles table
CREATE TABLE IF NOT EXISTS reaction_roles (
    message_id TEXT PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Warnings table
CREATE TABLE IF NOT EXISTS warnings (
    id SERIAL PRIMARY KEY,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    warnings JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Suggestions table
CREATE TABLE IF NOT EXISTS suggestions (
    message_id TEXT PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Whisper usage tracking table
CREATE TABLE IF NOT EXISTS whisper_usage (
    whisper_text TEXT PRIMARY KEY,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8-ball response usage tracking table
-- response_id is stable across text edits (e.g. "8ball_001")
-- response_text can be updated when wording changes
CREATE TABLE IF NOT EXISTS response_8ball_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vague statement usage tracking table
-- statement_id is stable across text edits (e.g. "vague_001")
-- statement_text can be updated when wording changes
CREATE TABLE IF NOT EXISTS response_vague_usage (
    statement_id TEXT PRIMARY KEY,
    statement_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_warnings_guild_user ON warnings(guild_id, user_id);
CREATE INDEX IF NOT EXISTS idx_whisper_usage_count ON whisper_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_whisper_last_used ON whisper_usage(last_used);
CREATE INDEX IF NOT EXISTS idx_8ball_usage_count ON response_8ball_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_8ball_last_used ON response_8ball_usage(last_used);
CREATE INDEX IF NOT EXISTS idx_vague_usage_count ON response_vague_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_vague_last_used ON response_vague_usage(last_used);
