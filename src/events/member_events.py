import discord
from discord.ext import commands
from config import SUPPORTER_ROLE
from database import load_prebans, save_prebans
from utils import log_moderation

class MemberEvents(commands.Cog):
    """Handle member-related events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Check if joining member is on the preban list"""
        prebans = load_prebans()
        guild_id = str(member.guild.id)
        user_id_str = str(member.id)

        if guild_id in prebans and user_id_str in prebans[guild_id]:
            preban_data = prebans[guild_id][user_id_str]
            reason = f"Preban: {preban_data['reason']}"

            try:
                # Silent ban - no DM, no public message
                await member.guild.ban(member, reason=reason, delete_message_days=0)

                # Remove from preban list (one-time use)
                del prebans[guild_id][user_id_str]
                save_prebans(prebans)

                # Notify mods in mod-logs
                await log_moderation(
                    member.guild,
                    "PREBAN TRIGGERED",
                    member.guild.me,  # Bot as the "moderator" who executed
                    member,
                    f"User joined and was automatically banned.\nOriginal preban reason: {preban_data['reason']}\nPreban added by: <@{preban_data['added_by']}>"
                )
            except discord.Forbidden:
                # Can't ban - log the failure
                mod_logs = discord.utils.get(member.guild.text_channels, name='mod-logs')
                if mod_logs:
                    embed = discord.Embed(
                        title="Preban Failed",
                        description=f"**User:** {member.mention} ({member.id})\n**Reason:** Insufficient permissions to ban\n**Original preban reason:** {preban_data['reason']}",
                        color=discord.Color.red()
                    )
                    await mod_logs.send(embed=embed)

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