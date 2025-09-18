import discord
from discord.ext import tasks
import random
from config import AHAMKARA_ACTIVITIES, STATUS_ROTATION_MINUTES

class StatusTasks:
    """Background tasks for status rotation"""

    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(minutes=STATUS_ROTATION_MINUTES)
    async def change_status(self):
        """Rotate through Ahamkara-themed statuses"""
        activity_type = random.choice([
            discord.ActivityType.watching,
            discord.ActivityType.listening,
            discord.ActivityType.playing
        ])

        activity_text = random.choice(AHAMKARA_ACTIVITIES)

        # Occasionally add "oh bearer mine" to the status
        if random.random() < 0.3:
            activity_text += ", o bearer mine"

        await self.bot.change_presence(
            activity=discord.Activity(type=activity_type, name=activity_text)
        )

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()