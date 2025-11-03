import discord
from discord.ext import commands
from database import load_reaction_roles
from config import COLOR_ROLES, EXOTIC_COLORS, SPECIAL_ROLES, PRONOUN_ROLES, DREAMER_ROLE

class ReactionEvents(commands.Cog):
    """Handle reaction role events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        reaction_data = load_reaction_roles()
        message_id = str(payload.message_id)

        if message_id not in reaction_data:
            return

        msg_data = reaction_data[message_id]
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if not member:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                return

        # VERIFICATION
        if msg_data['type'] == 'verify' and str(payload.emoji) == '✅':
            role = discord.utils.get(guild.roles, name=DREAMER_ROLE)
            if role and role not in member.roles:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    pass

        # COLOR ROLES
        elif msg_data['type'] in ['color', 'exotic']:
            emoji_str = str(payload.emoji)

            # Determine which color map to use
            if msg_data['type'] == 'color':
                color_map = COLOR_ROLES
            else:
                color_map = EXOTIC_COLORS

            if emoji_str in color_map:
                role_name = color_map[emoji_str]
                new_role = discord.utils.get(guild.roles, name=role_name)

                if new_role:
                    try:
                        # Remove all other color roles
                        all_color_names = list(COLOR_ROLES.values()) + list(EXOTIC_COLORS.values())
                        for color_name in all_color_names:
                            old_role = discord.utils.get(guild.roles, name=color_name)
                            if old_role and old_role in member.roles:
                                await member.remove_roles(old_role)

                        # Add new color
                        await member.add_roles(new_role)
                    except discord.Forbidden:
                        pass

        # SPECIAL ROLES
        elif msg_data['type'] == 'special':
            emoji_str = str(payload.emoji)

            if emoji_str in SPECIAL_ROLES:
                role_name = SPECIAL_ROLES[emoji_str]
                role = discord.utils.get(guild.roles, name=role_name)

                if role and role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        pass

        # PRONOUN ROLES
        elif msg_data['type'] == 'pronouns':
            emoji_str = str(payload.emoji)

            if emoji_str in PRONOUN_ROLES:
                role_name = PRONOUN_ROLES[emoji_str]
                role = discord.utils.get(guild.roles, name=role_name)

                if role and role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        reaction_data = load_reaction_roles()
        message_id = str(payload.message_id)

        if message_id not in reaction_data:
            return

        msg_data = reaction_data[message_id]

        # Handle color removal
        if msg_data['type'] in ['color', 'exotic']:
            emoji_str = str(payload.emoji)

            if msg_data['type'] == 'color':
                color_map = COLOR_ROLES
            else:
                color_map = EXOTIC_COLORS

            if emoji_str in color_map:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)

                if not member:
                    try:
                        member = await guild.fetch_member(payload.user_id)
                    except discord.NotFound:
                        return

                role_name = color_map[emoji_str]
                role = discord.utils.get(guild.roles, name=role_name)

                if role and role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except discord.Forbidden:
                        pass

        # Handle special role removal
        elif msg_data['type'] == 'special':
            emoji_str = str(payload.emoji)

            if emoji_str in SPECIAL_ROLES:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)

                if not member:
                    try:
                        member = await guild.fetch_member(payload.user_id)
                    except discord.NotFound:
                        return

                role_name = SPECIAL_ROLES[emoji_str]
                role = discord.utils.get(guild.roles, name=role_name)

                if role and role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except discord.Forbidden:
                        pass

        # Handle pronoun role removal
        elif msg_data['type'] == 'pronouns':
            emoji_str = str(payload.emoji)

            if emoji_str in PRONOUN_ROLES:
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)

                if not member:
                    try:
                        member = await guild.fetch_member(payload.user_id)
                    except discord.NotFound:
                        return

                role_name = PRONOUN_ROLES[emoji_str]
                role = discord.utils.get(guild.roles, name=role_name)

                if role and role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except discord.Forbidden:
                        pass

async def setup(bot):
    await bot.add_cog(ReactionEvents(bot))