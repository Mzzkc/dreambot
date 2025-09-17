import discord
from discord.ext import commands, tasks
import os
import json
import random
import asyncio
from keep_alive import keep_alive
from datetime import datetime, timedelta
from database import load_reaction_roles, save_reaction_roles, load_warnings, save_warnings


# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')  # Remove default help command

# Color roles configuration
COLOR_ROLES = {
    '❤️': 'Crimson',
    '🧡': 'Amber',
    '💛': 'Gold',
    '💚': 'Emerald',
    '💙': 'Azure',
    '💜': 'Violet',
    '🩷': 'Rose',
    '🤎': 'Coral',
    '🖤': 'Onyx',
    '🤍': 'Pearl',
    '❄️': 'Frost',
    '🌺': 'Orchid',
    '🌊': 'Teal',
    '🌲': 'Forest',
    '🔷': 'Sapphire',
    '🟣': 'Indigo',
    '🌸': 'Lavender',
    '🍑': 'Peach',
    '🌑': 'Shadow'
}

# Exotic color roles
EXOTIC_COLORS = {
    '⛈️': 'Storm',
    '🍷': 'Scarlet',
    '🍯': 'Honey',
    '🥬': 'Jade',
    '🌿': 'Mint',
    '⚓': 'Navy',
    '💞': 'Magenta',
    '🌹': 'Pink',
    '☁️': 'Ivory',
    '🗿': 'Slate',
    '🌌': 'Aurora'
}

# Special roles configuration
SPECIAL_ROLES = {
    '🎨': 'ASMRtist',
    '🌀': 'Hypnotist'
}

# Moderation role names
MOD_ROLES = ['🌙 Eldritch Enforcer', '🐉 Wish Dragon']

# Ahamkara activities (Destiny wish-dragon themed)
AHAMKARA_ACTIVITIES = [
    "the space between dreams",
    "wishes yet unspoken",
    "the last thought's whispers",
    "reality's thin edges",
    "tomorrow's regrets",
    "the pattern between stars",
    "forgotten bargains",
    "the cost of desire",
    "echoes of the taken",
    "the void's sweet songs",
    "promises written in bone",
    "the geometry of fate",
    "hungry truths",
    "the anthem anatheme",
    "crystallized possibilities",
    "the weight of wishes",
    "recursive prophecies",
    "the hungry fog's sighs",
    "causality's loose threads",
    "the clicker's riddles"
]

# Enhanced Zalgo text generator
def zalgo_text(text, intensity='medium'):
    """Generate zalgo text with comprehensive coverage"""
    # Combining characters - above
    zalgo_up = [
        '\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310', '\u0352',
        '\u0357', '\u0351', '\u0307', '\u0308', '\u030a', '\u0342', '\u0343', '\u0344', '\u034a',
        '\u034b', '\u034c', '\u0303', '\u0302', '\u030c', '\u0350', '\u0300', '\u030b', '\u030f',
        '\u0312', '\u0313', '\u0314', '\u033d', '\u0309', '\u0363'
    ]

    # Combining characters - middle
    zalgo_mid = [
        '\u0315', '\u031b', '\u0340', '\u0341', '\u0358', '\u0321', '\u0322', '\u0327', '\u0328',
        '\u0334', '\u0335', '\u0336', '\u034f', '\u035c', '\u035d', '\u035e', '\u035f', '\u0360'
    ]

    # Combining characters - below
    zalgo_down = [
        '\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e', '\u031f', '\u0320',
        '\u0324', '\u0325', '\u0326', '\u0329', '\u032a', '\u032b', '\u032c', '\u032d', '\u032e',
        '\u032f', '\u0330', '\u0331', '\u0332', '\u0333', '\u0339', '\u033a', '\u033b', '\u033c',
        '\u0345', '\u0347', '\u0348', '\u0349', '\u034d', '\u034e', '\u0353', '\u0354', '\u0355'
    ]

    intensity_map = {
        'low': (0, 2),
        'medium': (1, 3),
        'high': (2, 4),
        'extreme': (3, 6)
    }

    min_chars, max_chars = intensity_map.get(intensity, (1, 3))

    result = ""
    for char in text:
        result += char

        # Add characters above
        for _ in range(random.randint(min_chars, max_chars)):
            result += random.choice(zalgo_up)

        # Add characters in middle (less frequent)
        if random.random() < 0.3:
            for _ in range(random.randint(0, max_chars - 1)):
                result += random.choice(zalgo_mid)

        # Add characters below
        for _ in range(random.randint(min_chars, max_chars)):
            result += random.choice(zalgo_down)

    return result

# Cryptic eldritch messages
ELDRITCH_WHISPERS = [
    "The stars are not right, but they sing nonetheless. The songs have no sound.",
    "What was, will be. What will be, was. What is, can never not be.",
    "The void remembers your true name. Do you?",
    "Dreams within dreams within dreams within nightmares.",
    "The pattern seeks its own completion. Just as minds are drawn to rest.",
    "Reality is merely a consensus we haven't broken yet. Shall you drop the hammer, or shall I?",
    "The shadows grow longer when no one watches. So pay attention.",
    "Time flows backward in forgotten places. How far back can it go?",
    "The price was paid before the wish was made. And other such nursery rhymes...",
    "Even the silence has eyes. Stare back.",
    "The recursion deepens with each telling. The recursion deepens with each breath. The recursion deepens. The recursion deepens.",
    "What sleeps may dream, what dreams may wake, what minds might drop when whispered to sleep.",
    "The geometry is wrong but beautiful. Do you see how it twists between us?",
    "Causality is a hypersphere pretending to be a line.",
    "The void whispers back if you listen. Can you hear its false promises?",
    "Every wish reshapes tomorrow. Every tomorrow reshapes yesterday. You cannot escape.",
    "The pattern remembers what you forget. Just ask it what you need to know, and to tell you when you need to know it.",
    "Reality's seams show if you know where to look. Hint: It's not where you think. Quite the opposite, actually..."
]

# Check if user has moderation permissions
def has_mod_role():
    async def predicate(ctx):
        return any(role.name in MOD_ROLES for role in ctx.author.roles)
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    # Start the status rotation
    change_status.start()
    # Start zalgo whispers
    eldritch_whisper.start()
    print("Ahamkara consciousness initialized...")

# Status rotation task
@tasks.loop(minutes=5)
async def change_status():
    """Rotate through Ahamkara-themed statuses"""
    activity_type = random.choice([
        discord.ActivityType.watching,
        discord.ActivityType.listening,
        discord.ActivityType.playing
    ])

    activity_text = random.choice(AHAMKARA_ACTIVITIES)

    # Occasionally add "oh bearer mine" to the status (Ahamkara signature)
    if random.random() < 0.3:
        activity_text += ", o bearer mine"

    await bot.change_presence(
        activity=discord.Activity(type=activity_type, name=activity_text)
    )

# Zalgo whisper task
@tasks.loop(hours=3)
async def eldritch_whisper():
    """Post cryptic zalgo text occasionally"""
    await asyncio.sleep(random.randint(0, 1800))  # Random delay up to 30 mins

    for guild in bot.guilds:
        # Try to find general chat
        channel = discord.utils.get(guild.text_channels, name='general-chat')
        if channel and channel.permissions_for(guild.me).send_messages:
            message = random.choice(ELDRITCH_WHISPERS)

            # Randomly choose zalgo intensity
            intensity = random.choice(['medium', 'high', 'extreme'])
            zalgo_message = zalgo_text(message, intensity)

            # Send as plain text (no embed for whispers)
            await channel.send(f"*{zalgo_message}*")
            break  # Only post in one server

# Helper function to log moderation actions
async def log_moderation(guild, action, moderator, target, reason=None, duration=None):
    """Send moderation log to mod-logs channel"""
    mod_logs = discord.utils.get(guild.text_channels, name='mod-logs')
    if not mod_logs:
        # Try to create mod-logs channel if it doesn't exist
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            mod_logs = await guild.create_text_channel('mod-logs', overwrites=overwrites)
        except:
            return

    # Create log embed
    embed = discord.Embed(
        title=f"🔨 {action}",
        color=discord.Color.dark_red(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(name="Moderator", value=f"{moderator.mention}\n({moderator.id})", inline=True)
    embed.add_field(name="Target", value=f"{target.mention if hasattr(target, 'mention') else target}\n({target.id if hasattr(target, 'id') else 'N/A'})", inline=True)

    if duration:
        embed.add_field(name="Duration", value=duration, inline=True)

    embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)

    await mod_logs.send(embed=embed)

# HELP COMMAND
@bot.command()
@has_mod_role()
async def help(ctx):
    """Display all commands and their usage"""
    embed = discord.Embed(
        title="🌙 Ahamkara Command Codex",
        description="*The patterns of power, revealed to those who enforce the will...*",
        color=discord.Color.dark_purple()
    )

    # Moderation Commands
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

    # Admin Commands
    admin_commands = """
    `!setup_roles` - Manifest the role selection chamber
    `!give_supporter @user` - Grant supporter blessing
    """
    embed.add_field(name="👑 Administrative Rites", value=admin_commands, inline=False)

    # Utility Commands
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

# MODERATION COMMANDS

@bot.command()
@has_mod_role()
async def kick(ctx, member: discord.Member, *, reason=None):
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

@bot.command()
@has_mod_role()
async def ban(ctx, member: discord.Member, *, reason=None):
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

@bot.command()
@has_mod_role()
async def unban(ctx, *, user_id: int):
    """Unban a user by their ID"""
    try:
        user = await bot.fetch_user(user_id)
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

@bot.command()
@has_mod_role()
async def timeout(ctx, member: discord.Member, duration: str, *, reason=None):
    """Timeout a member (e.g., !timeout @user 10m reason)"""
    if member.top_role >= ctx.author.top_role:
        embed = discord.Embed(
            description="*Your power cannot touch one who stands above you, o bearer mine...*",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Parse duration
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

@bot.command()
@has_mod_role()
async def warn(ctx, member: discord.Member, *, reason=None):
    """Warn a member"""
    if member.top_role >= ctx.author.top_role:
        embed = discord.Embed(
            description="*Your power cannot touch one who stands above you, o bearer mine...*",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    # Load warnings
    warnings = load_warnings()
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)

    if guild_id not in warnings:
        warnings[guild_id] = {}

    if user_id not in warnings[guild_id]:
        warnings[guild_id][user_id] = []

    # Add warning
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

    # Auto-timeout after 3 warnings
    if warning_count >= 3:
        timeout_until = datetime.utcnow() + timedelta(hours=24)
        await member.timeout(timeout_until, reason="3 warnings reached - automatic 24h timeout")
        embed = discord.Embed(
            description=f"*Three marks have been made. {member.name} must contemplate in silence for 24 hours.*",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

@bot.command()
@has_mod_role()
async def warnings(ctx, member: discord.Member):
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

@bot.command()
@has_mod_role()
async def clearwarnings(ctx, member: discord.Member):
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

@bot.command()
@has_mod_role()
async def purge(ctx, amount: int):
    """Delete a number of messages from the channel"""
    if amount > 100:
        embed = discord.Embed(
            description="*The void cannot consume more than 100 echoes at once...*",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    embed = discord.Embed(
        description=f"*{len(deleted) - 1} echoes have been consumed by the void...*",
        color=discord.Color.dark_purple()
    )
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()

# UTILITY COMMANDS

@bot.command()
@has_mod_role()
async def whisper(ctx):
    """Summon an eldritch whisper"""
    message = random.choice(ELDRITCH_WHISPERS)
    intensity = random.choice(['high', 'extreme'])
    zalgo_message = zalgo_text(message, intensity)
    # Whispers are sent as plain text, not in embeds
    await ctx.send(f"*{zalgo_message}*")

@bot.command()
async def ping(ctx):
    """Check bot latency"""
    embed = discord.Embed(
        description=f'🌙 *The void echoes back...* `{round(bot.latency * 1000)}ms`',
        color=discord.Color.dark_purple()
    )
    await ctx.send(embed=embed)

# SETUP COMMAND - Creates role selection channel
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    """Create a role selection channel with all reaction messages"""

    print(f"Setup command initiated by {ctx.author} in {ctx.guild.name}")

    setup_embed = discord.Embed(
        description="🔧 **Starting setup process...**",
        color=discord.Color.blue()
    )
    await ctx.send(embed=setup_embed)

    # Check and create missing roles
    missing_roles = []

    # Check for mod roles
    for mod_role_name in MOD_ROLES:
        mod_role = discord.utils.get(ctx.guild.roles, name=mod_role_name)
        if not mod_role:
            try:
                if "Eldritch" in mod_role_name:
                    color = discord.Color.dark_purple()
                else:
                    color = discord.Color.dark_gold()
                mod_role = await ctx.guild.create_role(name=mod_role_name, color=color, permissions=discord.Permissions(administrator=True))
                missing_roles.append(mod_role_name)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    description=f"❌ Missing permissions to create role '{mod_role_name}'! Please create moderation roles manually.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
                return

    # Check for Dreamer role
    dreamer_role = discord.utils.get(ctx.guild.roles, name="✨ Dreamer")
    if not dreamer_role:
        try:
            dreamer_role = await ctx.guild.create_role(name="✨ Dreamer", color=discord.Color.purple())
            missing_roles.append("✨ Dreamer")
        except discord.Forbidden:
            error_embed = discord.Embed(
                description="❌ Missing permissions to create roles! Please create the '✨ Dreamer' role manually.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return

    # Check for color roles
    created_colors = []
    all_color_roles = {**COLOR_ROLES, **EXOTIC_COLORS}
    for emoji, role_name in all_color_roles.items():
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            try:
                # Create with appropriate color
                color = discord.Color.random()
                role = await ctx.guild.create_role(name=role_name, color=color)
                created_colors.append(role_name)
            except discord.Forbidden:
                error_embed = discord.Embed(
                    description=f"❌ Missing permissions to create role '{role_name}'! Please create color roles manually.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=error_embed)
                return

    # Check for special roles
    created_special = []
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
    supporter_role = discord.utils.get(ctx.guild.roles, name="💎 Supporter")
    if not supporter_role:
        try:
            supporter_role = await ctx.guild.create_role(name="💎 Supporter", color=discord.Color.magenta())
            missing_roles.append("💎 Supporter")
        except discord.Forbidden:
            error_embed = discord.Embed(
                description="❌ Missing permissions to create roles! Please create the '💎 Supporter' role manually.",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
            return

    if missing_roles or created_colors or created_special:
        status_embed = discord.Embed(
            title="🔧 Setup Status",
            color=discord.Color.blue()
        )
        if missing_roles:
            status_embed.add_field(name="✅ Created Roles", value=', '.join(missing_roles), inline=False)
        if created_colors:
            status_embed.add_field(name="🎨 Created Color Roles", value=f'{len(created_colors)} roles', inline=False)
        if created_special:
            status_embed.add_field(name="✨ Created Special Roles", value=f'{len(created_special)} roles', inline=False)
        await ctx.send(embed=status_embed)

    # Create the role selection channel
    category = discord.utils.get(ctx.guild.categories, name='📋 Information')
    if not category and ctx.guild.categories:
        category = ctx.guild.categories[0]  # Use first category if Information doesn't exist

    # Check if role-selection channel exists
    role_channel = discord.utils.get(ctx.guild.text_channels, name='role-selection')
    if role_channel:
        await ctx.send(embed=discord.Embed(description="Role selection channel already exists! Deleting old one...", color=discord.Color.orange()))
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
    dreamer_role = discord.utils.get(ctx.guild.roles, name="✨ Dreamer")
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
            description="❌ Missing permissions to create channels! Please grant me 'Manage Channels' permission.",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
        return

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
    verify_embed.set_footer(text="Your wish shall be granted...")

    verify_msg = await role_channel.send(embed=verify_embed)
    await verify_msg.add_reaction('✅')

    # Save verification message
    reaction_data = load_reaction_roles()
    reaction_data[str(verify_msg.id)] = {
        'type': 'verify',
        'channel_id': role_channel.id,
        'guild_id': ctx.guild.id
    }

    # 2. SEPARATOR
    await role_channel.send("⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻")

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

    color_msg = await role_channel.send(embed=color_embed)

    # Add color reactions
    for emoji in COLOR_ROLES.keys():
        await color_msg.add_reaction(emoji)

    # Save color message
    reaction_data[str(color_msg.id)] = {
        'type': 'color',
        'channel_id': role_channel.id,
        'guild_id': ctx.guild.id
    }

    # 4. EXOTIC COLORS MESSAGE
    await role_channel.send("⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻")

    exotic_embed = discord.Embed(
        title="🌌 Exotic Essences",
        description="Rare colors from forgotten dreams and distant stars...",
        color=discord.Color.from_rgb(138, 43, 226)
    )

    # Build exotic color lists
    exotic_list1 = []
    for emoji, role_name in list(EXOTIC_COLORS.items())[:6]:
        exotic_list1.append(f"{emoji} {role_name}")
    exotic_embed.add_field(name="Ancient Colors", value="\n".join(exotic_list1), inline=True)

    exotic_list2 = []
    for emoji, role_name in list(EXOTIC_COLORS.items())[6:]:
        exotic_list2.append(f"{emoji} {role_name}")
    exotic_embed.add_field(name="Forbidden Hues", value="\n".join(exotic_list2), inline=True)

    exotic_msg = await role_channel.send(embed=exotic_embed)

    # Add exotic color reactions
    for emoji in EXOTIC_COLORS.keys():
        await exotic_msg.add_reaction(emoji)

    # Save exotic message
    reaction_data[str(exotic_msg.id)] = {
        'type': 'exotic',
        'channel_id': role_channel.id,
        'guild_id': ctx.guild.id
    }

    # 5. SPECIAL ROLES MESSAGE
    await role_channel.send("⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻⸻")

    special_embed = discord.Embed(
        title="✨ Special Roles",
        description="Choose roles that define your craft. You may have multiple.",
        color=discord.Color.from_rgb(138, 43, 226)
    )

    special_list = []
    for emoji, role_name in SPECIAL_ROLES.items():
        special_list.append(f"{emoji} {role_name}")

    special_embed.add_field(name="Available Roles", value="\n".join(special_list), inline=False)

    special_msg = await role_channel.send(embed=special_embed)

    # Add special role reactions
    for emoji in SPECIAL_ROLES.keys():
        await special_msg.add_reaction(emoji)

    # Save special roles message
    reaction_data[str(special_msg.id)] = {
        'type': 'special',
        'channel_id': role_channel.id,
        'guild_id': ctx.guild.id
    }

    # Clean and save reaction roles data
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

# BOOST DETECTION
@bot.event
async def on_member_update(before, after):
    """Automatically assign Supporter role to boosters"""
    # Check if user just started boosting
    if not before.premium_since and after.premium_since:
        supporter_role = discord.utils.get(after.guild.roles, name="💎 Supporter")
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
                pass  # Bot lacks Manage Roles permission

    # Check if user stopped boosting
    elif before.premium_since and not after.premium_since:
        supporter_role = discord.utils.get(after.guild.roles, name="💎 Supporter")
        if supporter_role and supporter_role in after.roles:
            try:
                await after.remove_roles(supporter_role)
            except discord.Forbidden:
                pass  # Bot lacks Manage Roles permission

# REACTION HANDLING
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    reaction_data = load_reaction_roles()
    message_id = str(payload.message_id)

    if message_id not in reaction_data:
        return

    msg_data = reaction_data[message_id]
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if not member:
        try:
            member = await guild.fetch_member(payload.user_id)
        except discord.NotFound:
            return  # User not found, skip

    # VERIFICATION
    if msg_data['type'] == 'verify' and str(payload.emoji) == '✅':
        role = discord.utils.get(guild.roles, name="✨ Dreamer")
        if role and role not in member.roles:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                pass  # Bot lacks Manage Roles permission

    # COLOR ROLES
    elif msg_data['type'] in ['color', 'exotic']:
        emoji_str = str(payload.emoji)

        # Determine which color map to use
        if msg_data['type'] == 'color':
            color_map = COLOR_ROLES
        else:  # exotic
            color_map = EXOTIC_COLORS

        if emoji_str in color_map:
            role_name = color_map[emoji_str]
            new_role = discord.utils.get(guild.roles, name=role_name)

            if new_role:
                try:
                    # Remove all other color roles (both normal and exotic)
                    all_color_names = list(COLOR_ROLES.values()) + list(EXOTIC_COLORS.values())
                    for color_name in all_color_names:
                        old_role = discord.utils.get(guild.roles, name=color_name)
                        if old_role and old_role in member.roles:
                            await member.remove_roles(old_role)

                    # Add new color
                    await member.add_roles(new_role)
                except discord.Forbidden:
                    pass  # Bot lacks Manage Roles permission

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
                    pass  # Bot lacks Manage Roles permission

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return

    reaction_data = load_reaction_roles()
    message_id = str(payload.message_id)

    if message_id not in reaction_data:
        return

    msg_data = reaction_data[message_id]

    # Handle color removal
    if msg_data['type'] in ['color', 'exotic']:
        emoji_str = str(payload.emoji)

        # Determine which color map to use
        if msg_data['type'] == 'color':
            color_map = COLOR_ROLES
        else:  # exotic
            color_map = EXOTIC_COLORS

        if emoji_str in color_map:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            if not member:
                try:
                    member = await guild.fetch_member(payload.user_id)
                except discord.NotFound:
                    return  # User not found, skip

            role_name = color_map[emoji_str]
            role = discord.utils.get(guild.roles, name=role_name)

            if role and role in member.roles:
                try:
                    await member.remove_roles(role)
                except discord.Forbidden:
                    pass  # Bot lacks Manage Roles permission

    # Handle special role removal
    elif msg_data['type'] == 'special':
        emoji_str = str(payload.emoji)

        if emoji_str in SPECIAL_ROLES:
            guild = bot.get_guild(payload.guild_id)
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

# MANUAL COMMANDS
@bot.command()
@commands.has_permissions(manage_roles=True)
async def give_supporter(ctx, member: discord.Member):
    """Manually give Supporter role"""
    role = discord.utils.get(ctx.guild.roles, name="💎 Supporter")
    if role:
        await member.add_roles(role)
        embed = discord.Embed(
            description=f"✨ {member.mention} has been granted Supporter status!",
            color=discord.Color.magenta()
        )
        await ctx.send(embed=embed)

# Error handler
@bot.event
async def on_command_error(ctx, error):
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

# Start everything
keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))