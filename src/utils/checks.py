from discord.ext import commands
from config.constants import MOD_ROLES

def has_mod_role():
    """Check if user has moderation permissions"""
    async def predicate(ctx):
        return any(role.name in MOD_ROLES for role in ctx.author.roles)
    return commands.check(predicate)