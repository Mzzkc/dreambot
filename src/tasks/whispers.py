import discord
from discord.ext import tasks
import random
import asyncio
from utils import zalgo_text
from config import ELDRITCH_WHISPERS, ELDRITCH_WHISPER_HOURS, ELDRITCH_WHISPER_RANDOM_DELAY

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
                message = random.choice(ELDRITCH_WHISPERS)

                # Randomly choose zalgo intensity
                intensity = random.choice(['medium', 'high', 'extreme'])
                zalgo_message = zalgo_text(message, intensity)

                # Send as plain text (no embed for whispers)
                await channel.send(f"*{zalgo_message}*")
                break  # Only post in one server

    @eldritch_whisper.before_loop
    async def before_eldritch_whisper(self):
        await self.bot.wait_until_ready()