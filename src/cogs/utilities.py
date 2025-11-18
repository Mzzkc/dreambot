import discord
from discord.ext import commands
import random
from utils import has_mod_role, zalgo_text, zalgo_embed
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

async def setup(bot):
    await bot.add_cog(Utilities(bot))