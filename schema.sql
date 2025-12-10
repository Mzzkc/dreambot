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
-- whisper_id is stable across text edits (e.g. "whisper_001")
-- whisper_text can be updated when wording changes
CREATE TABLE IF NOT EXISTS whisper_usage (
    whisper_id TEXT PRIMARY KEY,
    whisper_text TEXT NOT NULL,
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

-- Prebans table (users to ban on join)
CREATE TABLE IF NOT EXISTS prebans (
    id SERIAL PRIMARY KEY,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(guild_id, user_id)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_prebans_guild_user ON prebans(guild_id, user_id);
CREATE INDEX IF NOT EXISTS idx_warnings_guild_user ON warnings(guild_id, user_id);
CREATE INDEX IF NOT EXISTS idx_whisper_usage_count ON whisper_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_whisper_last_used ON whisper_usage(last_used);
CREATE INDEX IF NOT EXISTS idx_8ball_usage_count ON response_8ball_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_8ball_last_used ON response_8ball_usage(last_used);
CREATE INDEX IF NOT EXISTS idx_vague_usage_count ON response_vague_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_vague_last_used ON response_vague_usage(last_used);

-- =============================================================================
-- INTENT-BASED RESPONSE POOL USAGE TABLES (Session 10-11)
-- Generic tables for tracking usage of intent-based response pools
-- =============================================================================

-- Phase 1 Core Intent Pools
CREATE TABLE IF NOT EXISTS response_greeting_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_gratitude_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_kebab_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_outlook_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_farewell_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_opinion_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_existential_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_meta_lore_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_challenge_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_animal_sound_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_affirmation_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_negation_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_exclamation_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Phase 2 Expanded Coverage Pools
CREATE TABLE IF NOT EXISTS response_self_statement_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_bot_capability_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_imperative_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_sharing_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_emotional_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_roleplay_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_correction_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_confusion_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Phase 3 Context-Aware Pools
CREATE TABLE IF NOT EXISTS response_kebab_intense_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_repetition_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_lore_callback_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS response_escape_usage (
    response_id TEXT PRIMARY KEY,
    response_text TEXT NOT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for intent pool tables (optional but recommended for larger datasets)
CREATE INDEX IF NOT EXISTS idx_greeting_usage_count ON response_greeting_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_kebab_usage_count ON response_kebab_usage(usage_count);
CREATE INDEX IF NOT EXISTS idx_opinion_usage_count ON response_opinion_usage(usage_count);
