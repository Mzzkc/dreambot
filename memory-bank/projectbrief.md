# Project Brief: Dreambot

## Purpose
An Ahamkara-themed Discord bot for server management, inspired by Destiny 2 lore. The bot speaks in the distinctive "o [bearer/dreamer/etc] mine" pattern and manages community wishes, roles, and moderation.

## Core Features
- **Wish/Suggestion System**: Users with Dreamer role can make wishes (video, channel, other) that get voted on
- **Reaction Roles**: Automated role assignment via reactions (verification, colors, special roles)
- **Moderation**: Warnings, kicks, bans, timeouts with logging
- **Eldritch Whispers**: Automated cryptic messages posted periodically
- **Role Management**: Complex role setup with color roles, exotic colors, special roles, and verification

## Theme
Ahamkara are wish-granting entities from Destiny lore - powerful, cunning, and dangerous. All bot interactions use lore-appropriate language:
- "o bearer mine", "o dreamer mine"
- References to patterns, the void, manifestation, geometry
- Cryptic, somewhat ominous tone while being helpful

## Tech Stack
- Python 3 with discord.py
- Supabase for database (PostgreSQL) with JSON file fallback
- Async task loops for periodic activities
- Cog-based architecture for modularity

## Success Criteria
- Smooth community wish fulfillment workflow
- Reliable role management
- Thematic consistency in all interactions
- Database reliability with graceful fallback
