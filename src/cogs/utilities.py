import discord
from discord.ext import commands
import random
from utils import has_mod_role, zalgo_text
from config import ELDRITCH_WHISPERS

class Utilities(commands.Cog):
    """Utility commands for various bot functions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_mod_role()
    async def whisper(self, ctx):
        """Summon an eldritch whisper"""
        message = random.choice(ELDRITCH_WHISPERS)
        intensity = random.choice(['high', 'extreme'])
        zalgo_message = zalgo_text(message, intensity)
        await ctx.send(f"*{zalgo_message}*")

    @commands.command()
    async def ping(self, ctx):
        """Check bot latency"""
        embed = discord.Embed(
            description=f'🌙 *The void echoes back...* `{round(self.bot.latency * 1000)}ms`',
            color=discord.Color.dark_purple()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))