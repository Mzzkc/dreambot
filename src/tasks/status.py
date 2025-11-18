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
        activity_text = random.choice(AHAMKARA_ACTIVITIES)

        # Occasionally add "oh bearer mine" to the status
        if random.random() < 0.3:
            activity_text += ", o bearer mine"

        # Randomly select activity type and create appropriate activity object
        choice = random.randint(1, 3)
        if choice == 1:
            # Playing - use Game for proper display
            activity = discord.Game(name=activity_text)
        elif choice == 2:
            # Watching
            activity = discord.Activity(type=discord.ActivityType.watching, name=activity_text)
        else:
            # Listening to
            activity = discord.Activity(type=discord.ActivityType.listening, name=activity_text)

        await self.bot.change_presence(activity=activity)

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()