import discord
from discord.ext import commands
from config import SUPPORTER_ROLE

class MemberEvents(commands.Cog):
    """Handle member-related events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Automatically assign Supporter role to boosters"""
        # Check if user just started boosting
        if not before.premium_since and after.premium_since:
            supporter_role = discord.utils.get(after.guild.roles, name=SUPPORTER_ROLE)
            if supporter_role and supporter_role not in after.roles:
                try:
                    await after.add_roles(supporter_role)

                    # Announce in general chat
                    general = discord.utils.get(after.guild.text_channels, name='general-chat')
                    if general:
                        embed = discord.Embed(
                            description=f"✨ **{after.mention} has blessed the server with a boost!** ✨\n*Their wishes shall be remembered...*",
                            color=discord.Color.magenta()
                        )
                        await general.send(embed=embed)
                except discord.Forbidden:
                    pass

        # Check if user stopped boosting
        elif before.premium_since and not after.premium_since:
            supporter_role = discord.utils.get(after.guild.roles, name=SUPPORTER_ROLE)
            if supporter_role and supporter_role in after.roles:
                try:
                    await after.remove_roles(supporter_role)
                except discord.Forbidden:
                    pass

async def setup(bot):
    await bot.add_cog(MemberEvents(bot))