import discord
from discord.ext import tasks
import random
import asyncio
from utils import zalgo_text
from config import ELDRITCH_WHISPERS, ELDRITCH_WHISPER_HOURS, ELDRITCH_WHISPER_RANDOM_DELAY
from database import load_whisper_usage, increment_whisper_usage


def select_weighted_whisper():
    """
    Select a whisper using weighted randomness that favors unselected whispers (ID-based).

    Weight formula: 1 / (usage_count + 1)^2
    - Unselected whispers (count=0) get weight = 1.0
    - First use (count=1) gets weight = 0.25
    - Second use (count=2) gets weight = 0.11
    - Third use (count=3) gets weight = 0.0625

    This makes it exponentially less likely to select frequently-used whispers.
    """
    usage_data = load_whisper_usage()

    # Calculate weights based on ID usage
    weights = []
    for whisper in ELDRITCH_WHISPERS:
        whisper_id = whisper["id"]
        usage_count = usage_data.get(whisper_id, {}).get('usage_count', 0)
        # Weight formula: inversely proportional to (usage_count + 1)^2
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    # Select whisper object and increment
    selected = random.choices(ELDRITCH_WHISPERS, weights=weights, k=1)[0]
    increment_whisper_usage(selected["id"], selected["text"])

    # Return just the text for display
    return selected["text"]


class WhisperTasks:
    """Background tasks for eldritch whispers"""

    def __init__(self, bot):
        self.bot = bot
        self.eldritch_whisper.start()

    def cog_unload(self):
        self.eldritch_whisper.cancel()

    @tasks.loop(hours=ELDRITCH_WHISPER_HOURS)
    async def eldritch_whisper(self):
        """Post cryptic zalgo text occasionally"""
        await asyncio.sleep(random.randint(0, ELDRITCH_WHISPER_RANDOM_DELAY))

        for guild in self.bot.guilds:
            # Try to find general chat
            channel = discord.utils.get(guild.text_channels, name='general-chat')
            if channel and channel.permissions_for(guild.me).send_messages:
                # Use weighted selection that favors unselected whispers
                message = select_weighted_whisper()

                # Randomly choose zalgo intensity
                intensity = random.choice(['medium', 'high', 'extreme'])
                zalgo_message = zalgo_text(message, intensity)

                # Send as plain text (no embed for whispers)
                await channel.send(f"*{zalgo_message}*")
                break  # Only post in one server

    @eldritch_whisper.before_loop
    async def before_eldritch_whisper(self):
        await self.bot.wait_until_ready()