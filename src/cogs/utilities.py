import discord
from discord.ext import commands
import random
import json
import re
import io
from datetime import datetime
from utils import has_mod_role, zalgo_text, zalgo_embed
from tasks.whispers import select_weighted_whisper

class Utilities(commands.Cog):
    """Utility commands for various bot functions"""

    def __init__(self, bot):
        self.bot = bot

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

        # Fetch all messages (oldest first for proper pairing)
        messages = []
        async for msg in channel.history(limit=limit, oldest_first=True):
            messages.append(msg)

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


async def setup(bot):
    await bot.add_cog(Utilities(bot))