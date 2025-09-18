import discord
from datetime import datetime

async def log_moderation(guild, action, moderator, target, reason=None, duration=None):
    """Send moderation log to mod-logs channel"""
    mod_logs = discord.utils.get(guild.text_channels, name='mod-logs')
    if not mod_logs:
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            mod_logs = await guild.create_text_channel('mod-logs', overwrites=overwrites)
        except:
            return

    embed = discord.Embed(
        title=f"🔨 {action}",
        color=discord.Color.dark_red(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="Moderator",
        value=f"{moderator.mention}\n({moderator.id})",
        inline=True
    )
    embed.add_field(
        name="Target",
        value=f"{target.mention if hasattr(target, 'mention') else target}\n({target.id if hasattr(target, 'id') else 'N/A'})",
        inline=True
    )

    if duration:
        embed.add_field(name="Duration", value=duration, inline=True)

    embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)

    await mod_logs.send(embed=embed)