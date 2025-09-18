import discord
from discord.ext import commands
import asyncio
from database import load_reaction_roles, save_reaction_roles
from config import (
    COLOR_ROLES, EXOTIC_COLORS, SPECIAL_ROLES,
    MOD_ROLES, DREAMER_ROLE, SUPPORTER_ROLE
)

class Roles(commands.Cog):
    """Role management and reaction roles"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_roles(self, ctx):
        """Create a role selection channel with all reaction messages"""
        print(f"Setup command initiated by {ctx.author} in {ctx.guild.name}")

        setup_embed = discord.Embed(
            description="🔧 **Starting setup process...**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=setup_embed)

        # Check and create missing roles
        missing_roles = []
        created_colors = []
        created_special = []

        # Check for mod roles
        for mod_role_name in MOD_ROLES:
            mod_role = discord.utils.get(ctx.guild.roles, name=mod_role_name)
            if not mod_role:
                try:
                    if "Eldritch" in mod_role_name:
                        color = discord.Color.dark_purple()
                    else:
                        color = discord.Color.dark_gold()
                    mod_role = await ctx.guild.create_role(
                        name=mod_role_name,
                        color=color,
                        permissions=discord.Permissions(administrator=True)
                    )
                    missing_roles.append(mod_role_name)
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        description=f"❌ Missing permissions to create role '{mod_role_name}'!",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=error_embed)
                    return

        # Check for Dreamer role
        dreamer_role = discord.utils.get(ctx.guild.roles, name=DREAMER_ROLE)
        if not dreamer_role:
            try:
                dreamer_role = await ctx.guild.create_role(
                    name=DREAMER_ROLE,
                    color=discord.Color.purple()
                )
                missing_roles.append(DREAMER_ROLE)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    description=f"❌ Missing permissions to create roles!",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
                return

        # Check for color roles
        all_color_roles = {**COLOR_ROLES, **EXOTIC_COLORS}
        for emoji, role_name in all_color_roles.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                try:
                    color = discord.Color.random()
                    role = await ctx.guild.create_role(name=role_name, color=color)
                    created_colors.append(role_name)
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        description=f"❌ Missing permissions to create role '{role_name}'!",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=error_embed)
                    return

        # Check for special roles
        for emoji, role_name in SPECIAL_ROLES.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                try:
                    color = discord.Color.random()
                    role = await ctx.guild.create_role(name=role_name, color=color)
                    created_special.append(role_name)
                except discord.Forbidden:
                    error_embed = discord.Embed(
                        description=f"❌ Missing permissions to create role '{role_name}'!",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=error_embed)
                    return

        # Check for Supporter role
        supporter_role = discord.utils.get(ctx.guild.roles, name=SUPPORTER_ROLE)
        if not supporter_role:
            try:
                supporter_role = await ctx.guild.create_role(
                    name=SUPPORTER_ROLE,
                    color=discord.Color.magenta()
                )
                missing_roles.append(SUPPORTER_ROLE)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    description="❌ Missing permissions to create roles!",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
                return

        # Report created roles
        if missing_roles or created_colors or created_special:
            status_embed = discord.Embed(
                title="🔧 Setup Status",
                color=discord.Color.blue()
            )
            if missing_roles:
                status_embed.add_field(
                    name="✅ Created Roles",
                    value=', '.join(missing_roles),
                    inline=False
                )
            if created_colors:
                status_embed.add_field(
                    name="🎨 Created Color Roles",
                    value=f'{len(created_colors)} roles',
                    inline=False
                )
            if created_special:
                status_embed.add_field(
                    name="✨ Created Special Roles",
                    value=f'{len(created_special)} roles',
                    inline=False
                )
            await ctx.send(embed=status_embed)

        # Create the role selection channel
        category = discord.utils.get(ctx.guild.categories, name='📋 Information')
        if not category and ctx.guild.categories:
            category = ctx.guild.categories[0]

        # Check if role-selection channel exists
        role_channel = discord.utils.get(ctx.guild.text_channels, name='role-selection')
        if role_channel:
            await ctx.send(embed=discord.Embed(
                description="Role selection channel already exists! Deleting old one...",
                color=discord.Color.orange()
            ))
            await role_channel.delete()
            await asyncio.sleep(1)

        # Create new role selection channel
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False,
                add_reactions=True
            ),
            ctx.guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                add_reactions=True,
                manage_messages=True
            )
        }

        # Add permission for Dreamer role if it exists
        dreamer_role = discord.utils.get(ctx.guild.roles, name=DREAMER_ROLE)
        if dreamer_role:
            overwrites[dreamer_role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False,
                add_reactions=True
            )

        try:
            if category:
                role_channel = await category.create_text_channel(
                    'role-selection',
                    overwrites=overwrites,
                    topic="React to get roles! | Verification, Colors & Special Roles"
                )
            else:
                role_channel = await ctx.guild.create_text_channel(
                    'role-selection',
                    overwrites=overwrites,
                    topic="React to get roles! | Verification, Colors & Special Roles"
                )
        except discord.Forbidden:
            error_embed = discord.Embed(
                description="❌ Missing permissions to create channels!",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return

        # Setup reaction messages
        reaction_data = await self._setup_reaction_messages(role_channel, ctx.guild.id)
        save_reaction_roles(reaction_data)

        print(f"Setup completed successfully for {ctx.guild.name}")

        complete_embed = discord.Embed(
            title="✅ Setup Complete!",
            description=f"🔗 Role selection channel: {role_channel.mention}\n🎭 All roles configured and ready!",
            color=discord.Color.green()
        )
        complete_embed.add_field(
            name="📝 How to use",
            value="• New members: React with ✅ to verify\n• Color roles: React with color emojis (one only)\n• Special roles: React for your talents (multiple allowed)",
            inline=False
        )
        await ctx.send(embed=complete_embed)

    async def _setup_reaction_messages(self, channel, guild_id):
        """Setup all reaction role messages in the channel"""
        reaction_data = {}

        # 1. VERIFICATION MESSAGE
        verify_embed = discord.Embed(
            title="🌙 Server Verification",
            description=(
                "**Welcome, o seeker mine...**\n\n"
                "Before you can access the server, you must acknowledge our covenant.\n"
                "Read the rules in #welcome-and-rules first.\n\n"
                "✅ **React below to receive the Dreamer role and enter our realm**"
            ),
            color=discord.Color.dark_purple()
        )
        verify_embed.set_footer(text="Your wishes shall be granted...")

        verify_msg = await channel.send(embed=verify_embed)
        await verify_msg.add_reaction('✅')

        reaction_data[str(verify_msg.id)] = {
            'type': 'verify',
            'channel_id': channel.id,
            'guild_id': guild_id
        }

        # 2. SEPARATOR
        await channel.send("⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻")

        # 3. COLOR ROLES MESSAGE
        color_embed = discord.Embed(
            title="🎨 Choose Your Essence",
            description="Your color reflects your inner nature. Choose wisely, for you may hold only one.",
            color=discord.Color.gold()
        )

        # Build color lists
        color_list1 = []
        for emoji, role_name in list(COLOR_ROLES.items())[:10]:
            color_list1.append(f"{emoji} {role_name}")
        color_embed.add_field(name="Primary Essence", value="\n".join(color_list1), inline=True)

        color_list2 = []
        for emoji, role_name in list(COLOR_ROLES.items())[10:]:
            color_list2.append(f"{emoji} {role_name}")
        color_embed.add_field(name="Rare Essence", value="\n".join(color_list2), inline=True)

        color_msg = await channel.send(embed=color_embed)

        for emoji in COLOR_ROLES.keys():
            await color_msg.add_reaction(emoji)

        reaction_data[str(color_msg.id)] = {
            'type': 'color',
            'channel_id': channel.id,
            'guild_id': guild_id
        }

        # 4. EXOTIC COLORS MESSAGE
        await channel.send("⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻")

        exotic_embed = discord.Embed(
            title="🌌 Exotic Essences",
            description="Rare colors from forgotten dreams and distant stars...",
            color=discord.Color.from_rgb(138, 43, 226)
        )

        exotic_list1 = []
        for emoji, role_name in list(EXOTIC_COLORS.items())[:6]:
            exotic_list1.append(f"{emoji} {role_name}")
        exotic_embed.add_field(name="Ancient Colors", value="\n".join(exotic_list1), inline=True)

        exotic_list2 = []
        for emoji, role_name in list(EXOTIC_COLORS.items())[6:]:
            exotic_list2.append(f"{emoji} {role_name}")
        exotic_embed.add_field(name="Forbidden Hues", value="\n".join(exotic_list2), inline=True)

        exotic_msg = await channel.send(embed=exotic_embed)

        for emoji in EXOTIC_COLORS.keys():
            await exotic_msg.add_reaction(emoji)

        reaction_data[str(exotic_msg.id)] = {
            'type': 'exotic',
            'channel_id': channel.id,
            'guild_id': guild_id
        }

        # 5. SPECIAL ROLES MESSAGE
        await channel.send("⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻")

        special_embed = discord.Embed(
            title="✨ Special Roles",
            description="Choose roles that define your craft. You may have multiple.",
            color=discord.Color.from_rgb(138, 43, 226)
        )

        special_list = []
        for emoji, role_name in SPECIAL_ROLES.items():
            special_list.append(f"{emoji} {role_name}")

        special_embed.add_field(name="Available Roles", value="\n".join(special_list), inline=False)

        special_msg = await channel.send(embed=special_embed)

        for emoji in SPECIAL_ROLES.keys():
            await special_msg.add_reaction(emoji)

        reaction_data[str(special_msg.id)] = {
            'type': 'special',
            'channel_id': channel.id,
            'guild_id': guild_id
        }

        return reaction_data

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def give_supporter(self, ctx, member: discord.Member):
        """Manually give Supporter role"""
        role = discord.utils.get(ctx.guild.roles, name=SUPPORTER_ROLE)
        if role:
            await member.add_roles(role)
            embed = discord.Embed(
                description=f"✨ {member.mention} has been granted Supporter status!",
                color=discord.Color.magenta()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Roles(bot))