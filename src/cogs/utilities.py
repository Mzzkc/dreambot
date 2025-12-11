import discord
from discord.ext import commands
import asyncio
import random
import json
import re
import io
import logging
from datetime import datetime
from utils import has_mod_role, zalgo_text, zalgo_embed
from tasks.whispers import select_weighted_whisper
from config import DREAMER_ROLE, MOD_ROLES

logger = logging.getLogger(__name__)

# Rate limit handling for message fetching
# Discord allows ~50 requests/second but we stay conservative
HARVEST_BATCH_SIZE = 100  # Fetch 100 messages at a time
HARVEST_BATCH_DELAY = 0.5  # 500ms between batches

class Utilities(commands.Cog):
    """Utility commands for various bot functions"""

    def __init__(self, bot):
        self.bot = bot
        self.help_cooldowns = {}  # For help command cooldown

    async def has_dreamer_role(self, member):
        """Check if member has Dreamer role or higher"""
        dreamer_role = discord.utils.get(member.roles, name=DREAMER_ROLE)
        mod_roles = [discord.utils.get(member.roles, name=role) for role in MOD_ROLES]
        return dreamer_role or any(mod_roles)

    @commands.command()
    @has_mod_role()
    async def whisper(self, ctx):
        """Summon an eldritch whisper (uses weighted selection)"""
        # Use weighted selection (same algorithm as periodic whispers)
        message = select_weighted_whisper()
        intensity = random.choice(['high', 'extreme'])
        zalgo_message = zalgo_text(message, intensity)
        await ctx.send(f"*{zalgo_message}*")

    @commands.command()
    @has_mod_role()
    async def speak(self, ctx, *, message: str):
        """Make the bot speak in #general-chat (admin only)"""
        # Find general-chat channel
        general_chat = discord.utils.get(ctx.guild.text_channels, name='general-chat')

        if not general_chat:
            embed = zalgo_embed(
                description="I cannot find the general-chat to manifest my words, o bearer mine...",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Transform message to zalgo
        zalgo_message = zalgo_text(message, intensity='medium')

        # Send to general-chat
        await general_chat.send(f"*{zalgo_message}*")

        # Confirm to admin (with zalgo confirmation)
        confirmation = zalgo_text("Your words echo through the void, o bearer mine...", intensity='low')
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency"""
        embed = zalgo_embed(
            description=f'🌙 The void echoes back... {round(self.bot.latency * 1000)}ms',
            color=discord.Color.dark_purple()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def harvest(self, ctx, channel_name: str = "bot-spam", limit: int = None):
        """
        Harvest conversation data from a channel for chatbot training.

        Collects all @bot mentions and their responses, strips user data,
        outputs as JSONL for LLM analysis.

        Usage: !harvest [channel_name] [limit]
        Example: !harvest bot-spam 1000
        """
        # Find target channel
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
        if not channel:
            embed = zalgo_embed(
                description=f"Cannot find #{channel_name}, o bearer mine...",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Acknowledge the request
        status_msg = await ctx.send(f"🔮 Harvesting conversations from #{channel_name}...")

        # Fetch messages in batches to avoid rate limits
        messages = []
        total_fetched = 0
        last_message = None

        while True:
            batch = []
            # Fetch a batch (oldest_first for proper pairing)
            async for msg in channel.history(
                limit=HARVEST_BATCH_SIZE,
                before=last_message,
                oldest_first=False  # We'll reverse later
            ):
                batch.append(msg)

            if not batch:
                break

            messages.extend(batch)
            total_fetched += len(batch)
            last_message = batch[-1]

            # Update status periodically
            if total_fetched % 500 == 0:
                await status_msg.edit(content=f"🔮 Fetched {total_fetched} messages...")

            # Rate limit delay between batches
            await asyncio.sleep(HARVEST_BATCH_DELAY)

            # Check if we've hit the user-specified limit
            if limit and total_fetched >= limit:
                messages = messages[:limit]
                break

        # Reverse to get oldest first (we fetched newest first in batches)
        messages.reverse()

        await status_msg.edit(content=f"🔮 Processing {len(messages)} messages...")

        # Build call/response pairs
        interactions = []
        i = 0
        while i < len(messages):
            msg = messages[i]

            # Check if this message mentions the bot
            if self.bot.user in msg.mentions and msg.author != self.bot.user:
                # Extract clean content (strip mentions)
                clean_content = re.sub(r'<@!?\d+>', '', msg.content).strip()

                # Skip empty messages after stripping mentions
                if not clean_content:
                    i += 1
                    continue

                # Classify as question or statement
                msg_type = "q" if self._is_question(clean_content) else "s"

                # Look for bot's response (next message from bot)
                response_content = None
                for j in range(i + 1, min(i + 10, len(messages))):  # Look within next 10 messages
                    if messages[j].author == self.bot.user:
                        # Strip zalgo/formatting for cleaner analysis
                        response_content = self._clean_response(messages[j].content)
                        break

                if response_content:
                    interactions.append({
                        "ts": msg.created_at.isoformat(),
                        "q": clean_content,
                        "t": msg_type,
                        "a": response_content
                    })

            i += 1

        if not interactions:
            embed = zalgo_embed(
                description="No conversations found to harvest, o bearer mine...",
                color=discord.Color.orange()
            )
            await status_msg.edit(content=None, embed=embed)
            return

        # Format as JSONL
        jsonl_lines = [json.dumps(item, ensure_ascii=False) for item in interactions]
        jsonl_content = "\n".join(jsonl_lines)

        # Create file for DM
        file_buffer = io.StringIO(jsonl_content)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dreambot_conversations_{timestamp}.jsonl"

        # DM to invoker
        try:
            dm_channel = await ctx.author.create_dm()
            await dm_channel.send(
                content=f"🐉 Harvested {len(interactions)} conversations from #{channel_name}",
                file=discord.File(io.BytesIO(jsonl_content.encode('utf-8')), filename=filename)
            )

            embed = zalgo_embed(
                description=f"Harvested {len(interactions)} conversations. Check your DMs, o bearer mine...",
                color=discord.Color.green()
            )
            await status_msg.edit(content=None, embed=embed)

        except discord.Forbidden:
            # Can't DM - send in channel instead
            await ctx.send(
                content=f"🐉 Harvested {len(interactions)} conversations",
                file=discord.File(io.BytesIO(jsonl_content.encode('utf-8')), filename=filename)
            )
            await status_msg.delete()

    def _is_question(self, text):
        """Detect if a message is a question (same logic as message_events)"""
        text_lower = text.lower().strip()

        if '?' in text_lower:
            return True

        modal_patterns = [
            r'^(will|would|should|could|can|may|might|shall|must)\s+\w+',
            r'^(is|are|was|were|am|has|have|had|do|does|did)\s+\w+',
        ]
        for pattern in modal_patterns:
            if re.match(pattern, text_lower):
                return True

        return False

    def _clean_response(self, content):
        """Strip zalgo and formatting from bot response for analysis"""
        # Remove italics markers
        clean = content.strip('*').strip('_')

        # Remove zalgo combining characters (diacritics)
        # Unicode ranges for combining diacritical marks
        clean = re.sub(r'[\u0300-\u036f\u0489]', '', clean)

        return clean.strip()

    @commands.command()
    async def help(self, ctx, *, command: str = None):
        """*Reveal the patterns of power available to you...*"""
        # Cooldown check (5 minutes)
        user_id = ctx.author.id
        current_time = datetime.utcnow()

        if user_id in self.help_cooldowns:
            last_used = self.help_cooldowns[user_id]
            if (current_time - last_used).total_seconds() < 300:  # 5 minutes
                time_left = 300 - (current_time - last_used).total_seconds()
                embed = discord.Embed(
                    description=f"*The patterns require {int(time_left)} more seconds to align...*",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed, delete_after=5)
                return

        self.help_cooldowns[user_id] = current_time

        # Check if user is mod/admin
        is_mod = any(role.name in MOD_ROLES for role in ctx.author.roles)

        if is_mod:
            # Show full help for mods/admins
            embed = discord.Embed(
                title="🌙 Ahamkara Command Codex",
                description="*The patterns of power, revealed to those who enforce the will...*",
                color=discord.Color.dark_purple()
            )

            mod_commands = """
            `!kick @user [reason]` - Cast a soul into the void
            `!ban @user [reason]` - Erase a pattern from reality
            `!unban user_id` - Restore a banished soul
            `!timeout @user duration [reason]` - Silence a voice (10s/5m/2h/1d)
            `!warn @user [reason]` - Mark a transgression
            `!warnings @user` - View marks upon a soul
            `!clearwarnings @user` - Erase all marks
            `!purge amount` - Consume messages (max 100)
            `!preban user_id [reason]` - Mark for erasure upon arrival
            `!unpreban user_id` - Lift the mark of erasure
            `!prebans` - View all marked patterns
            """
            embed.add_field(name="⚔️ Enforcement Powers", value=mod_commands, inline=False)

            admin_commands = """
            `!setup_roles` - Manifest the role selection chamber
            `!give_supporter @user` - Grant supporter blessing
            """
            embed.add_field(name="👑 Administrative Rites", value=admin_commands, inline=False)

            suggestion_commands = """
            `!wish <type> <description>` - Shape reality through desire
            `!topvideos [limit]` - Reveal most desired active visions
            `!topchannels [limit]` - Reveal most desired active realms
            `!topother [limit]` - Unveil whispered active possibilities
            `!manifestations [type] [limit]` - View granted wishes
            `!setthreshold <value>` - Adjust manifestation threshold
            `!manifestwish <id> [notes]` - Mark a wish as granted
            `!removewish <message_id>` - Unmake a wish from the pattern
            `!weeklysummary` - Post weekly summary (testing)
            `!migratewishes` - Update existing wishes (run once after upgrade)
            """
            embed.add_field(name="✨ Wish Manifestation", value=suggestion_commands, inline=False)

            util_commands = """
            `!whisper` - Summon an eldritch whisper
            `!speak <message>` - Manifest zalgo whispers to #general-chat
            `!harvest [channel] [limit]` - Harvest conversation data for analysis
            `!ping` - Test the void's echo
            `!help` - Reveal this codex
            """
            embed.add_field(name="🔮 Arcane Utilities", value=util_commands, inline=False)

            interactive_features = """
            `@Dreambot <question>` - Receive cryptic prophecy (35 responses)
            `@Dreambot <statement>` - Receive vague acknowledgment (29 responses)
            • All responses manifest through extreme zalgo transformation
            • Weighted selection favors variety in responses
            """
            embed.add_field(name="🎱 Interactive Manifestations", value=interactive_features, inline=False)

            embed.add_field(
                name="📝 Notes",
                value="• Only **🌙 Eldritch Enforcer** and **🐉 Wish Dragon** may wield these powers\n• Warnings auto-timeout after 3 marks (24h)\n• All actions are logged to #mod-logs",
                inline=False
            )

            embed.set_footer(text="Your wishes shape reality, o bearer mine...")
        else:
            # Show limited help for regular users
            embed = discord.Embed(
                title="🌙 Available Patterns",
                description="*These powers are yours to command, o dreamer mine...*",
                color=discord.Color.purple()
            )

            # Check if user has dreamer role
            has_dreamer = await self.has_dreamer_role(ctx.author)

            if has_dreamer:
                wish_commands = """
                `!wish video <description>` - Weave visions into reality
                `!wish channel <name: purpose>` - Manifest new realms of discourse
                `!wish other <description>` - Shape possibility through desire
                """
                embed.add_field(name="✨ Dream Manifestation", value=wish_commands, inline=False)

            info_commands = """
            `!topvideos [limit]` - Witness the most coveted active visions
            `!topchannels [limit]` - Witness the most desired active realms
            `!topother [limit]` - Glimpse whispered active possibilities
            `!manifestations [type] [limit]` - View granted wishes
            `!ping` - Test the void's echo
            """
            embed.add_field(name="🔮 Arcane Knowledge", value=info_commands, inline=False)

            interactive_features = """
            `@Dreambot <question>` - Receive cryptic prophecy (35 responses)
            `@Dreambot <statement>` - Receive vague acknowledgment (29 responses)
            • All responses manifest through extreme zalgo transformation
            • Weighted selection favors variety in responses
            """
            embed.add_field(name="🎱 Interactive Manifestations", value=interactive_features, inline=False)

            if not has_dreamer:
                embed.add_field(
                    name="💫 Path to Ascension",
                    value="*Seek the ✨ Dreamer blessing to weave reality through desire, o aspiring mine...*",
                    inline=False
                )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utilities(bot))