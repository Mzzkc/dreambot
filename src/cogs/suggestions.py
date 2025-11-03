import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
from database import db
from config import DREAMER_ROLE, MOD_ROLES
from utils import has_mod_role

class Suggestions(commands.Cog):
    """Ahamkara suggestion system for wishes and desires"""

    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}  # For help command cooldown
        self.vote_threshold = 0.67  # 2/3 threshold for channel creation
        self.suggestions_channel_name = "suggestions"
        self.community_category_name = "💬 Community"

        # Start weekly summary task
        self.weekly_summary.start()

    def cog_unload(self):
        self.weekly_summary.cancel()

    async def has_dreamer_role(self, member):
        """Check if member has Dreamer role or higher"""
        dreamer_role = discord.utils.get(member.roles, name=DREAMER_ROLE)
        mod_roles = [discord.utils.get(member.roles, name=role) for role in MOD_ROLES]
        return dreamer_role or any(mod_roles)

    def get_suggestions_channel(self, guild):
        """Get the suggestions channel"""
        return discord.utils.get(guild.channels, name=self.suggestions_channel_name)

    def get_community_category(self, guild):
        """Get the community category"""
        return discord.utils.get(guild.categories, name=self.community_category_name)

    @commands.command(name='wish')
    async def wish_command(self, ctx, wish_type: str, *, description: str):
        """*Make a wish, o bearer mine...*

        Types: video, channel, other
        For channel wishes: Use format 'channel_name: description'
        """
        # Check if user has Dreamer role or higher
        if not await self.has_dreamer_role(ctx.author):
            embed = discord.Embed(
                description="*Only those who dream may shape reality, o aspiring mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Check if we're in the suggestions channel
        suggestions_channel = self.get_suggestions_channel(ctx.guild)
        if not suggestions_channel:
            embed = discord.Embed(
                description="*The realm of wishes has not been established...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if ctx.channel != suggestions_channel:
            embed = discord.Embed(
                description=f"*Wishes must be whispered in {suggestions_channel.mention}, o bearer mine...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        wish_type = wish_type.lower()
        if wish_type not in ['video', 'channel', 'other']:
            embed = discord.Embed(
                description="*The pattern recognizes only: video, channel, other...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Delete the original command message
        await ctx.message.delete()

        # Handle different wish types
        if wish_type == 'channel':
            await self._handle_channel_wish(ctx, description)
        elif wish_type == 'video':
            await self._handle_video_wish(ctx, description)
        else:  # other
            await self._handle_other_wish(ctx, description)

    async def _handle_video_wish(self, ctx, description):
        """Handle video suggestion"""
        embed = discord.Embed(
            title="🎬 Video Wish",
            description=f"*A vision dances in the void...*\n\n{description}",
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"Wished by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="React with 🌟 to support this wish")

        message = await ctx.send(embed=embed)
        await message.add_reaction('🌟')

        # Save to database
        self._save_suggestion(str(message.id), 'video', ctx.author.id, description, ctx.guild.id, ctx.channel.id)

    async def _handle_channel_wish(self, ctx, description):
        """Handle channel suggestion"""
        # Parse channel name and description
        if ':' not in description:
            embed = discord.Embed(
                description="*Channel wishes require form: channel_name: description*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=5)
            return

        channel_name, channel_desc = description.split(':', 1)
        channel_name = channel_name.strip()
        channel_desc = channel_desc.strip()

        embed = discord.Embed(
            title="💬 Channel Wish",
            description=f"*A new realm seeks manifestation...*\n\n**Channel:** {channel_name}\n**Purpose:** {channel_desc}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"Wished by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="React with 🌟 to support this wish")

        message = await ctx.send(embed=embed)
        await message.add_reaction('🌟')

        # Save to database
        full_desc = f"{channel_name}: {channel_desc}"
        self._save_suggestion(str(message.id), 'channel', ctx.author.id, full_desc, ctx.guild.id, ctx.channel.id)

    async def _handle_other_wish(self, ctx, description):
        """Handle other suggestion"""
        embed = discord.Embed(
            title="✨ Other Wish",
            description=f"*The void whispers of possibilities...*\n\n{description}",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"Wished by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="React with 🌟 to support this wish")

        message = await ctx.send(embed=embed)
        await message.add_reaction('🌟')

        # Save to database
        self._save_suggestion(str(message.id), 'other', ctx.author.id, description, ctx.guild.id, ctx.channel.id)

    def _save_suggestion(self, message_id: str, suggestion_type: str, author_id: int, description: str, guild_id: int, channel_id: int):
        """Save suggestion to database"""
        suggestions = self._load_suggestions()
        suggestions[message_id] = {
            'type': suggestion_type,
            'author_id': author_id,
            'description': description,
            'guild_id': guild_id,
            'channel_id': channel_id,
            'votes': 0,
            'created_at': datetime.utcnow().isoformat()
        }
        self._save_suggestions_to_db(suggestions)

    def _load_suggestions(self) -> Dict:
        """Load suggestions from database"""
        if not db.supabase:
            try:
                with open('suggestions.json', 'r') as f:
                    return json.load(f)
            except:
                return {}

        try:
            response = db.supabase.table('suggestions').select("*").execute()
            return {item['message_id']: item['data'] for item in response.data}
        except:
            return {}

    def _save_suggestions_to_db(self, data: Dict):
        """Save suggestions to database"""
        if not db.supabase:
            with open('suggestions.json', 'w') as f:
                json.dump(data, f)
            return

        try:
            # Clear existing
            db.supabase.table('suggestions').delete().neq('message_id', '0').execute()

            # Insert new data
            for message_id, suggestion_data in data.items():
                db.supabase.table('suggestions').upsert({
                    'message_id': message_id,
                    'data': suggestion_data
                }).execute()
        except Exception as e:
            print(f"Database error, falling back to JSON: {e}")
            with open('suggestions.json', 'w') as f:
                json.dump(data, f)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle voting on suggestions"""
        if user.bot or str(reaction.emoji) != '🌟':
            return

        suggestions = self._load_suggestions()
        message_id = str(reaction.message.id)

        if message_id in suggestions:
            suggestions[message_id]['votes'] = reaction.count - 1  # Subtract bot's reaction
            self._save_suggestions_to_db(suggestions)

            # Check if channel suggestion meets threshold
            suggestion = suggestions[message_id]
            if suggestion['type'] == 'channel':
                await self._check_channel_threshold(reaction.message, suggestion)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """Handle vote removal on suggestions"""
        if user.bot or str(reaction.emoji) != '🌟':
            return

        suggestions = self._load_suggestions()
        message_id = str(reaction.message.id)

        if message_id in suggestions:
            suggestions[message_id]['votes'] = max(0, reaction.count - 1)  # Subtract bot's reaction
            self._save_suggestions_to_db(suggestions)

    async def _check_channel_threshold(self, message, suggestion):
        """Check if channel suggestion meets voting threshold"""
        guild = message.guild
        member_count = len([m for m in guild.members if not m.bot])
        threshold_votes = int(member_count * self.vote_threshold)

        if suggestion['votes'] >= threshold_votes:
            # Create the channel
            await self._create_suggested_channel(message, suggestion)

    async def _create_suggested_channel(self, message, suggestion):
        """Create a channel from suggestion"""
        guild = message.guild
        category = self.get_community_category(guild)

        if not category:
            embed = discord.Embed(
                description="*The Community realm does not exist to house this wish...*",
                color=discord.Color.red()
            )
            await message.reply(embed=embed)
            return

        # Parse channel name
        description = suggestion['description']
        channel_name, _ = description.split(':', 1)
        channel_name = channel_name.strip().lower().replace(' ', '-')

        try:
            new_channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                reason=f"Channel created by wish fulfillment (votes: {suggestion['votes']})"
            )

            embed = discord.Embed(
                title="🌟 Wish Fulfilled!",
                description=f"*The pattern manifests: {new_channel.mention} has been created!*",
                color=discord.Color.green()
            )
            await message.reply(embed=embed)

            # Remove suggestion from database
            suggestions = self._load_suggestions()
            del suggestions[str(message.id)]
            self._save_suggestions_to_db(suggestions)

        except Exception as e:
            embed = discord.Embed(
                description=f"*The wish could not be fulfilled: {str(e)}*",
                color=discord.Color.red()
            )
            await message.reply(embed=embed)

    @commands.command(name='topvideos')
    async def top_videos(self, ctx, limit: int = 10):
        """*List the most desired video visions...*"""
        suggestions = self._load_suggestions()
        video_suggestions = [
            (msg_id, data) for msg_id, data in suggestions.items()
            if data['type'] == 'video' and data['guild_id'] == ctx.guild.id
        ]

        # Sort by votes
        video_suggestions.sort(key=lambda x: x[1]['votes'], reverse=True)
        video_suggestions = video_suggestions[:limit]

        if not video_suggestions:
            embed = discord.Embed(
                description="*No video visions dance in the void...*",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🎬 Top Video Wishes",
            description="*The most desired visions...*",
            color=discord.Color.purple()
        )

        for i, (msg_id, data) in enumerate(video_suggestions, 1):
            embed.add_field(
                name=f"{i}. {data['votes']} 🌟",
                value=data['description'][:100] + ('...' if len(data['description']) > 100 else ''),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name='topother')
    async def top_other(self, ctx, limit: int = 10):
        """*List the most desired other wishes...*"""
        suggestions = self._load_suggestions()
        other_suggestions = [
            (msg_id, data) for msg_id, data in suggestions.items()
            if data['type'] == 'other' and data['guild_id'] == ctx.guild.id
        ]

        # Sort by votes
        other_suggestions.sort(key=lambda x: x[1]['votes'], reverse=True)
        other_suggestions = other_suggestions[:limit]

        if not other_suggestions:
            embed = discord.Embed(
                description="*No other desires whisper in the darkness...*",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="✨ Top Other Wishes",
            description="*The most whispered possibilities...*",
            color=discord.Color.gold()
        )

        for i, (msg_id, data) in enumerate(other_suggestions, 1):
            embed.add_field(
                name=f"{i}. {data['votes']} 🌟",
                value=data['description'][:100] + ('...' if len(data['description']) > 100 else ''),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name='setthreshold')
    @has_mod_role()
    async def set_threshold(self, ctx, threshold: float):
        """*Adjust the voting threshold for channel creation...*"""
        if not 0.1 <= threshold <= 1.0:
            embed = discord.Embed(
                description="*Threshold must dance between 0.1 and 1.0...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        self.vote_threshold = threshold
        embed = discord.Embed(
            description=f"*Channel creation threshold set to {threshold:.0%}*",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='migratewishes')
    @has_mod_role()
    async def migrate_wishes(self, ctx):
        """*Migrate existing wishes to include channel information...*

        This command backfills channel_id for suggestions created before the update.
        Only needed once after upgrading the bot.
        """
        suggestions = self._load_suggestions()
        suggestions_channel = self.get_suggestions_channel(ctx.guild)

        if not suggestions_channel:
            embed = discord.Embed(
                description="*The realm of wishes does not exist...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        status_embed = discord.Embed(
            title="🔄 Migration in Progress",
            description="*Reweaving the pattern to include the paths of origin...*",
            color=discord.Color.blue()
        )
        status_msg = await ctx.send(embed=status_embed)

        migrated = 0
        already_migrated = 0
        failed = 0

        for message_id, data in suggestions.items():
            # Check if already has channel_id
            if 'channel_id' in data:
                already_migrated += 1
                continue

            # Try to fetch the message and get its channel_id
            try:
                message = await suggestions_channel.fetch_message(int(message_id))
                data['channel_id'] = message.channel.id
                migrated += 1
            except Exception as e:
                # Message not found or error - default to suggestions channel
                data['channel_id'] = suggestions_channel.id
                failed += 1

        # Save updated suggestions
        if migrated > 0 or failed > 0:
            self._save_suggestions_to_db(suggestions)

        # Report results
        result_embed = discord.Embed(
            title="✅ Migration Complete",
            color=discord.Color.green()
        )
        result_embed.add_field(
            name="Results",
            value=f"**Migrated:** {migrated}\n**Already Complete:** {already_migrated}\n**Defaulted:** {failed}",
            inline=False
        )
        result_embed.set_footer(text="All wishes now contain their paths of origin")

        await status_msg.edit(embed=result_embed)

    @commands.command(name='removewish')
    @has_mod_role()
    async def remove_wish(self, ctx, message_id: str):
        """*Unmake a wish, erasing it from the pattern...*

        Usage: !removewish <message_id>
        You can right-click a message and copy its ID, or use the message link.
        """
        # Extract message ID from Discord link if provided
        if 'discord.com/channels/' in message_id:
            message_id = message_id.split('/')[-1]

        suggestions = self._load_suggestions()

        if message_id not in suggestions:
            embed = discord.Embed(
                description="*This wish does not exist in the pattern...*",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Get suggestion details before deletion for confirmation
        suggestion = suggestions[message_id]
        wish_type = suggestion['type']

        # Remove from database
        del suggestions[message_id]
        self._save_suggestions_to_db(suggestions)

        # Try to delete the message if we're in the suggestions channel
        try:
            suggestions_channel = self.get_suggestions_channel(ctx.guild)
            if suggestions_channel:
                message = await suggestions_channel.fetch_message(int(message_id))
                await message.delete()
        except:
            pass  # Message might already be deleted or inaccessible

        embed = discord.Embed(
            title="🌑 Wish Erased",
            description=f"*The {wish_type} wish has been unmade, its pattern dissolved into the void...*",
            color=discord.Color.dark_gray()
        )
        await ctx.send(embed=embed)

    @tasks.loop(hours=168)  # Run weekly (168 hours)
    async def weekly_summary(self):
        """Send weekly summary of top suggestions"""
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            suggestions_channel = self.get_suggestions_channel(guild)
            if not suggestions_channel:
                continue

            suggestions = self._load_suggestions()
            guild_suggestions = {
                msg_id: data for msg_id, data in suggestions.items()
                if data['guild_id'] == guild.id
            }

            # Get top video and other suggestions
            video_suggestions = [(msg_id, data) for msg_id, data in guild_suggestions.items() if data['type'] == 'video']
            other_suggestions = [(msg_id, data) for msg_id, data in guild_suggestions.items() if data['type'] == 'other']

            video_suggestions.sort(key=lambda x: x[1]['votes'], reverse=True)
            other_suggestions.sort(key=lambda x: x[1]['votes'], reverse=True)

            embed = discord.Embed(
                title="📅 Weekly Wish Summary",
                description="*The pattern reveals the most desired manifestations...*",
                color=discord.Color.dark_purple(),
                timestamp=datetime.utcnow()
            )

            # Top video wishes
            if video_suggestions:
                video_text = ""
                for i, (msg_id, data) in enumerate(video_suggestions[:5], 1):
                    # Get channel_id, default to suggestions channel if not present
                    channel_id = data.get('channel_id', suggestions_channel.id)
                    message_link = f"https://discord.com/channels/{guild.id}/{channel_id}/{msg_id}"
                    video_text += f"{i}. **{data['votes']} 🌟** - [View Wish]({message_link})\n*{data['description'][:80]}{'...' if len(data['description']) > 80 else ''}*\n\n"
                embed.add_field(name="🎬 Top Video Wishes", value=video_text, inline=False)

            # Top other wishes
            if other_suggestions:
                other_text = ""
                for i, (msg_id, data) in enumerate(other_suggestions[:5], 1):
                    # Get channel_id, default to suggestions channel if not present
                    channel_id = data.get('channel_id', suggestions_channel.id)
                    message_link = f"https://discord.com/channels/{guild.id}/{channel_id}/{msg_id}"
                    other_text += f"{i}. **{data['votes']} 🌟** - [View Wish]({message_link})\n*{data['description'][:80]}{'...' if len(data['description']) > 80 else ''}*\n\n"
                embed.add_field(name="✨ Top Other Wishes", value=other_text, inline=False)

            if video_suggestions or other_suggestions:
                await suggestions_channel.send(embed=embed)

    @weekly_summary.before_loop
    async def before_weekly_summary(self):
        """Wait for the bot to be ready before starting the weekly summary"""
        await self.bot.wait_until_ready()

        # Calculate next Monday at midnight
        now = datetime.utcnow()
        days_ahead = 0 - now.weekday()  # Monday is 0
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7

        next_monday = now + timedelta(days=days_ahead)
        next_monday = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)

        # Wait until next Monday
        wait_seconds = (next_monday - now).total_seconds()
        await asyncio.sleep(wait_seconds)

    @commands.command()
    async def help(self, ctx, *, command: str = None):
        """*Reveal the patterns of power available to you...*"""
        # Cooldown check (5 minutes)
        user_id = ctx.author.id
        current_time = datetime.utcnow()

        if user_id in self.cooldowns:
            last_used = self.cooldowns[user_id]
            if (current_time - last_used).total_seconds() < 300:  # 5 minutes
                time_left = 300 - (current_time - last_used).total_seconds()
                embed = discord.Embed(
                    description=f"*The patterns require {int(time_left)} more seconds to align...*",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed, delete_after=5)
                return

        self.cooldowns[user_id] = current_time

        # Check if user is mod/admin
        is_mod = any(role.name in MOD_ROLES for role in ctx.author.roles)

        if is_mod:
            # Show full help for mods/admins
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

            suggestion_commands = """
            `!wish <type> <description>` - Shape reality through desire
            `!topvideos [limit]` - Reveal most desired visions
            `!topother [limit]` - Unveil whispered possibilities
            `!setthreshold <value>` - Adjust manifestation threshold
            `!removewish <message_id>` - Unmake a wish from the pattern
            `!migratewishes` - Update existing wishes (run once after upgrade)
            """
            embed.add_field(name="✨ Wish Manifestation", value=suggestion_commands, inline=False)

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
        else:
            # Show limited help for regular users
            embed = discord.Embed(
                title="🌙 Available Patterns",
                description="*These powers are yours to command, o dreamer mine...*",
                color=discord.Color.purple()
            )

            # Check if user has dreamer role
            has_dreamer = await self.has_dreamer_role(ctx.author)

            if has_dreamer:
                wish_commands = """
                `!wish video <description>` - Weave visions into reality
                `!wish channel <name: purpose>` - Manifest new realms of discourse
                `!wish other <description>` - Shape possibility through desire
                """
                embed.add_field(name="✨ Dream Manifestation", value=wish_commands, inline=False)

            info_commands = """
            `!topvideos [limit]` - Witness the most coveted visions
            `!topother [limit]` - Glimpse whispered possibilities
            `!ping` - Test the void's echo
            """
            embed.add_field(name="🔮 Arcane Knowledge", value=info_commands, inline=False)

            if not has_dreamer:
                embed.add_field(
                    name="💫 Path to Ascension",
                    value="*Seek the ✨ Dreamer blessing to weave reality through desire, o aspiring mine...*",
                    inline=False
                )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))