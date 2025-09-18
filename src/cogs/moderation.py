import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from utils import has_mod_role, log_moderation
from database import load_warnings, save_warnings
from config import AUTO_TIMEOUT_WARNINGS, AUTO_TIMEOUT_DURATION_HOURS, PURGE_MAX_MESSAGES

class Moderation(commands.Cog):
    """Moderation commands for server management"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_mod_role()
    async def help(self, ctx):
        """Display all commands and their usage"""
        embed = discord.Embed(
            title="🌙 Ahamkara Command Codex",
            description="*The patterns of power, revealed to those who enforce the will...*",
            color=discord.Color.dark_purple()
        )

        mod_commands = """
        `!kick @user [reason]` - Cast a soul into the void
        `!ban @user [reason]` - Erase a pattern from reality
        `!unban user_id` - Restore a banished soul
        `!timeout @user duration [reason]` - Silence a voice (10s/5m/2h/1d)
        `!warn @user [reason]` - Mark a transgression
        `!warnings @user` - View marks upon a soul
        `!clearwarnings @user` - Erase all marks
        `!purge amount` - Consume messages (max 100)
        """
        embed.add_field(name="⚔️ Enforcement Powers", value=mod_commands, inline=False)

        admin_commands = """
        `!setup_roles` - Manifest the role selection chamber
        `!give_supporter @user` - Grant supporter blessing
        """
        embed.add_field(name="👑 Administrative Rites", value=admin_commands, inline=False)

        util_commands = """
        `!whisper` - Summon an eldritch whisper
        `!ping` - Test the void's echo
        `!help` - Reveal this codex
        """
        embed.add_field(name="🔮 Arcane Utilities", value=util_commands, inline=False)

        embed.add_field(
            name="📝 Notes",
            value="• Only **🌙 Eldritch Enforcer** and **🐉 Wish Dragon** may wield these powers\n• Warnings auto-timeout after 3 marks (24h)\n• All actions are logged to #mod-logs",
            inline=False
        )

        embed.set_footer(text="Your wishes shape reality, o bearer mine...")
        await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                description="*Your power cannot touch one who stands above you, o bearer mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                description=f"*{member.name} has been cast into the void... Their wishes go unanswered.*",
                color=discord.Color.dark_purple()
            )
            await ctx.send(embed=embed)
            await log_moderation(ctx.guild, "KICK", ctx.author, member, reason)
        except discord.Forbidden:
            embed = discord.Embed(
                description="*My power is insufficient for this wish...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server"""
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                description="*Your power cannot touch one who stands above you, o bearer mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                description=f"*{member.name} has been erased from this reality. Their pattern is broken.*",
                color=discord.Color.dark_purple()
            )
            await ctx.send(embed=embed)
            await log_moderation(ctx.guild, "BAN", ctx.author, member, reason)
        except discord.Forbidden:
            embed = discord.Embed(
                description="*My power is insufficient for this wish...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def unban(self, ctx, *, user_id: int):
        """Unban a user by their ID"""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                description=f"*{user.name} may walk these paths again. Their pattern is restored.*",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            await log_moderation(ctx.guild, "UNBAN", ctx.author, user)
        except discord.NotFound:
            embed = discord.Embed(
                description="*This soul does not exist in the void...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                description="*My power is insufficient for this wish...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason=None):
        """Timeout a member (e.g., !timeout @user 10m reason)"""
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                description="*Your power cannot touch one who stands above you, o bearer mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            time_amount = int(duration[:-1])
            time_unit = duration[-1]
            if time_unit not in time_convert:
                embed = discord.Embed(
                    description="*Invalid time unit. Use s/m/h/d.*",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            seconds = time_amount * time_convert[time_unit]
            timeout_until = datetime.utcnow() + timedelta(seconds=seconds)

            await member.timeout(timeout_until, reason=reason)
            embed = discord.Embed(
                description=f"*{member.name} has been silenced. Their voice echoes in the void for {duration}.*",
                color=discord.Color.dark_purple()
            )
            await ctx.send(embed=embed)
            await log_moderation(ctx.guild, "TIMEOUT", ctx.author, member, reason, duration)
        except:
            embed = discord.Embed(
                description="*Invalid duration format. Use: 10s, 5m, 2h, or 1d*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """Warn a member"""
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                description="*Your power cannot touch one who stands above you, o bearer mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        warnings = load_warnings()
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in warnings:
            warnings[guild_id] = {}

        if user_id not in warnings[guild_id]:
            warnings[guild_id][user_id] = []

        warning_data = {
            'reason': reason or 'No reason provided',
            'moderator': ctx.author.id,
            'timestamp': datetime.now().isoformat()
        }

        warnings[guild_id][user_id].append(warning_data)
        save_warnings(warnings)

        warning_count = len(warnings[guild_id][user_id])

        embed = discord.Embed(
            description=f"*{member.name} has been marked. This is warning #{warning_count}. The pattern remembers...*",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        await log_moderation(ctx.guild, f"WARNING (#{warning_count})", ctx.author, member, reason)

        if warning_count >= AUTO_TIMEOUT_WARNINGS:
            timeout_until = datetime.utcnow() + timedelta(hours=AUTO_TIMEOUT_DURATION_HOURS)
            await member.timeout(timeout_until, reason=f"{AUTO_TIMEOUT_WARNINGS} warnings reached - automatic {AUTO_TIMEOUT_DURATION_HOURS}h timeout")
            embed = discord.Embed(
                description=f"*Three marks have been made. {member.name} must contemplate in silence for {AUTO_TIMEOUT_DURATION_HOURS} hours.*",
                color=discord.Color.dark_red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def warnings(self, ctx, member: discord.Member):
        """Check warnings for a member"""
        warnings = load_warnings()
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in warnings or user_id not in warnings[guild_id]:
            embed = discord.Embed(
                description=f"*{member.name} bears no marks in this reality.*",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

        user_warnings = warnings[guild_id][user_id]

        embed = discord.Embed(
            title=f"📜 Marks upon {member.name}",
            color=discord.Color.orange()
        )

        for i, warning in enumerate(user_warnings, 1):
            timestamp = datetime.fromisoformat(warning['timestamp']).strftime('%Y-%m-%d %H:%M')
            mod = ctx.guild.get_member(warning['moderator'])
            mod_name = mod.name if mod else f"Unknown ({warning['moderator']})"

            embed.add_field(
                name=f"Warning #{i} - {timestamp}",
                value=f"**By:** {mod_name}\n**Reason:** {warning['reason']}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def clearwarnings(self, ctx, member: discord.Member):
        """Clear all warnings for a member"""
        warnings = load_warnings()
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id in warnings and user_id in warnings[guild_id]:
            del warnings[guild_id][user_id]
            save_warnings(warnings)
            embed = discord.Embed(
                description=f"*The marks upon {member.name} have been erased. Their pattern is clean.*",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            await log_moderation(ctx.guild, "WARNINGS CLEARED", ctx.author, member)
        else:
            embed = discord.Embed(
                description=f"*{member.name} bears no marks to erase.*",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @has_mod_role()
    async def purge(self, ctx, amount: int):
        """Delete a number of messages from the channel"""
        if amount > PURGE_MAX_MESSAGES:
            embed = discord.Embed(
                description=f"*The void cannot consume more than {PURGE_MAX_MESSAGES} echoes at once...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            description=f"*{len(deleted) - 1} echoes have been consumed by the void...*",
            color=discord.Color.dark_purple()
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()

async def setup(bot):
    await bot.add_cog(Moderation(bot))