import discord
from discord.ext import commands
import os
import asyncio
from config import BOT_PREFIX, INTENTS
from tasks.status import StatusTasks
from tasks.whispers import WhisperTasks

class DreambotClient(commands.Bot):
    """Custom bot class with integrated functionality"""

    def __init__(self):
        super().__init__(command_prefix=BOT_PREFIX, intents=INTENTS)
        self.remove_command('help')  # Remove default help command
        self.status_tasks = None
        self.whisper_tasks = None

    async def setup_hook(self):
        """This is called when the bot is starting up"""
        # Load cogs
        cogs = [
            'cogs.moderation',
            'cogs.roles',
            'cogs.utilities',
            'events.member_events',
            'events.reaction_events'
        ]

        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")

        # Start background tasks
        self.status_tasks = StatusTasks(self)
        self.whisper_tasks = WhisperTasks(self)

    async def on_ready(self):
        """Called when the bot is ready"""
        print(f'{self.user} is online!')
        print("Ahamkara consciousness initialized...")

    async def on_command_error(self, ctx, error):
        """Global error handler"""
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                description="*Only the Eldritch Enforcers and Wish Dragons may wield this power, o bearer mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="*Your wishes exceed your power, o ambitious mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                description="*The pattern does not recognize this form...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            pass  # Ignore unknown commands
        else:
            print(f"Error: {error}")

def create_bot():
    """Factory function to create bot instance"""
    return DreambotClient()