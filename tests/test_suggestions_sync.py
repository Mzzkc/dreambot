"""
Unit tests for suggestion reaction count synchronization

Tests the sync_reaction_counts method which reconciles database counts
with actual Discord message reactions after bot restarts.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, Mock, patch
import discord


@pytest.fixture
def mock_bot():
    """Create a mock Discord bot"""
    bot = AsyncMock()
    bot.user = Mock()
    bot.user.id = 123456789
    return bot


@pytest.fixture
def mock_guild(mock_suggestions_channel):
    """Create a mock Discord guild"""
    guild = Mock(spec=discord.Guild)
    guild.id = 987654321
    guild.name = "Test Guild"

    # Create mock members (10 non-bot members)
    members = []
    for i in range(10):
        member = Mock()
        member.bot = False
        members.append(member)

    # Add a bot member
    bot_member = Mock()
    bot_member.bot = True
    members.append(bot_member)

    guild.members = members
    # Return mock channel by default
    guild.get_channel = Mock(return_value=mock_suggestions_channel)

    return guild


@pytest.fixture
def mock_suggestions_channel():
    """Create a mock suggestions channel"""
    channel = AsyncMock(spec=discord.TextChannel)
    channel.id = 111222333
    channel.name = "suggestions"
    return channel


@pytest.fixture
def suggestions_cog(mock_bot, mock_suggestions_channel):
    """Create a Suggestions cog instance with mocked dependencies"""
    with patch('sys.path', ['/home/emzi/Projects/dreambot/src'] + __import__('sys').path):
        from cogs.suggestions import Suggestions

        # Mock the task loop start to prevent event loop issues
        with patch.object(Suggestions, '__init__', lambda self, bot: None):
            cog = Suggestions(mock_bot)
            cog.bot = mock_bot
            cog.cooldowns = {}
            cog.vote_threshold = 0.67
            cog.suggestions_channel_name = "suggestions"
            cog.community_category_name = "💬 Community"
            cog.get_suggestions_channel = Mock(return_value=mock_suggestions_channel)
            cog.get_community_category = Mock()

            return cog


def create_mock_message(message_id, reaction_count):
    """Helper to create a mock Discord message with reactions"""
    message = AsyncMock(spec=discord.Message)
    message.id = message_id

    # Create mock reaction
    reaction = Mock(spec=discord.Reaction)
    reaction.emoji = '🌟'
    reaction.count = reaction_count  # Includes bot's reaction

    message.reactions = [reaction]
    return message


def create_discord_not_found():
    """Helper to create a proper discord.NotFound exception"""
    response = Mock()
    response.status = 404
    response.text = ""
    return discord.NotFound(response, "")


def create_discord_forbidden():
    """Helper to create a proper discord.Forbidden exception"""
    response = Mock()
    response.status = 403
    response.text = ""
    return discord.Forbidden(response, "")


@pytest.mark.asyncio
async def test_sync_updates_stale_counts(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync correctly updates stale vote counts"""

    # Setup: DB has stale count (5), Discord has actual count (8)
    mock_suggestions = {
        '111111': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 5,  # Stale count
            'status': 'active',
            'description': 'Test video wish'
        }
    }

    # Mock message with 9 reactions (8 real + 1 bot)
    mock_message = create_mock_message(111111, 9)
    mock_suggestions_channel.fetch_message = AsyncMock(return_value=mock_message)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Count was updated
    assert stats['synced'] == 1
    assert stats['deleted'] == 0
    assert stats['errors'] == 0

    # Verify: Database save was called
    suggestions_cog._save_suggestions_to_db.assert_called_once()

    # Verify: Updated count is correct (9 reactions - 1 bot = 8 votes)
    saved_data = suggestions_cog._save_suggestions_to_db.call_args[0][0]
    assert saved_data['111111']['votes'] == 8


@pytest.mark.asyncio
async def test_sync_removes_deleted_messages(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync removes wishes whose messages were deleted"""

    # Setup: DB has wish but message is deleted
    mock_suggestions = {
        '222222': {
            'type': 'other',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 10,
            'status': 'active',
            'description': 'Deleted wish'
        }
    }

    # Mock fetch_message raising NotFound
    mock_suggestions_channel.fetch_message = AsyncMock(side_effect=create_discord_not_found())

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Message was deleted from DB
    assert stats['synced'] == 0
    assert stats['deleted'] == 1
    assert stats['errors'] == 0

    # Verify: Database save was called
    suggestions_cog._save_suggestions_to_db.assert_called_once()

    # Verify: Wish was removed
    saved_data = suggestions_cog._save_suggestions_to_db.call_args[0][0]
    assert '222222' not in saved_data


@pytest.mark.asyncio
async def test_sync_handles_missing_channels(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync gracefully handles missing channels"""

    # Setup: DB has wish in non-existent channel
    mock_suggestions = {
        '333333': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 999999999,  # Non-existent channel
            'votes': 5,
            'status': 'active',
            'description': 'Wish in missing channel'
        }
    }

    # Mock guild.get_channel returning None
    mock_guild.get_channel = Mock(return_value=None)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Error was counted, no crash
    assert stats['synced'] == 0
    assert stats['deleted'] == 0
    assert stats['errors'] == 1

    # Verify: Database was NOT saved (no changes)
    suggestions_cog._save_suggestions_to_db.assert_not_called()


@pytest.mark.asyncio
async def test_sync_handles_permission_errors(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync gracefully handles permission errors"""

    # Setup: DB has wish but bot lacks permission
    mock_suggestions = {
        '444444': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 5,
            'status': 'active',
            'description': 'Forbidden wish'
        }
    }

    # Mock fetch_message raising Forbidden
    mock_suggestions_channel.fetch_message = AsyncMock(side_effect=create_discord_forbidden())

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Error was counted, no crash
    assert stats['synced'] == 0
    assert stats['deleted'] == 0
    assert stats['errors'] == 1


@pytest.mark.asyncio
async def test_sync_auto_manifests_channel_at_threshold(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync auto-manifests channel wishes at threshold"""

    # Setup: Channel wish with 7+ votes (70% threshold met)
    # Guild has 10 members, threshold is 67%, so need 7 votes
    mock_suggestions = {
        '555555': {
            'type': 'channel',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 3,  # Stale count
            'status': 'active',
            'description': 'test-channel: A new channel'
        }
    }

    # Mock message with 8 reactions (7 real + 1 bot) = meets threshold
    mock_message = create_mock_message(555555, 8)
    mock_suggestions_channel.fetch_message = AsyncMock(return_value=mock_message)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Mock channel creation
    suggestions_cog._create_suggested_channel = AsyncMock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Channel was auto-manifested
    assert stats['synced'] == 1
    assert stats['manifested'] == 1

    # Verify: _create_suggested_channel was called
    suggestions_cog._create_suggested_channel.assert_called_once()


@pytest.mark.asyncio
async def test_sync_does_not_manifest_below_threshold(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync does NOT manifest channel wishes below threshold"""

    # Setup: Channel wish with 5 votes (below 67% threshold)
    mock_suggestions = {
        '666666': {
            'type': 'channel',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 2,  # Stale count
            'status': 'active',
            'description': 'low-vote-channel: Not enough votes'
        }
    }

    # Mock message with 6 reactions (5 real + 1 bot) = below threshold
    mock_message = create_mock_message(666666, 6)
    mock_suggestions_channel.fetch_message = AsyncMock(return_value=mock_message)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Mock channel creation
    suggestions_cog._create_suggested_channel = AsyncMock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Count was updated but channel NOT manifested
    assert stats['synced'] == 1
    assert stats['manifested'] == 0

    # Verify: _create_suggested_channel was NOT called
    suggestions_cog._create_suggested_channel.assert_not_called()


@pytest.mark.asyncio
async def test_sync_ignores_granted_wishes(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync only processes active wishes, ignoring granted ones"""

    # Setup: Mix of active and granted wishes
    mock_suggestions = {
        '777777': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 5,
            'status': 'active',
            'description': 'Active wish'
        },
        '888888': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 10,
            'status': 'granted',  # Already granted
            'description': 'Granted wish'
        }
    }

    # Mock message for active wish
    mock_message = create_mock_message(777777, 8)
    mock_suggestions_channel.fetch_message = AsyncMock(return_value=mock_message)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Only active wish was processed
    assert stats['synced'] == 1

    # Verify: fetch_message called only once (for active wish)
    assert mock_suggestions_channel.fetch_message.call_count == 1
    mock_suggestions_channel.fetch_message.assert_called_with(777777)


@pytest.mark.asyncio
async def test_sync_multiple_wishes_mixed_scenarios(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test sync handling multiple wishes with different scenarios"""

    # Setup: Multiple wishes with different scenarios
    mock_suggestions = {
        '111111': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 5,
            'status': 'active',
            'description': 'Needs update'
        },
        '222222': {
            'type': 'other',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 10,
            'status': 'active',
            'description': 'Deleted message'
        },
        '333333': {
            'type': 'video',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 8,
            'status': 'active',
            'description': 'Already accurate'
        },
        '444444': {
            'type': 'channel',
            'guild_id': 987654321,
            'channel_id': 111222333,
            'votes': 2,
            'status': 'active',
            'description': 'ready-channel: Meets threshold'
        }
    }

    # Mock fetch_message with different responses
    async def mock_fetch(message_id):
        if message_id == 111111:
            return create_mock_message(111111, 9)  # Count changed
        elif message_id == 222222:
            raise create_discord_not_found()  # Deleted
        elif message_id == 333333:
            return create_mock_message(333333, 9)  # Same count (8 votes + 1 bot)
        elif message_id == 444444:
            return create_mock_message(444444, 8)  # Meets threshold (7 votes + 1 bot)

    mock_suggestions_channel.fetch_message = AsyncMock(side_effect=mock_fetch)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Mock channel creation
    suggestions_cog._create_suggested_channel = AsyncMock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify statistics
    assert stats['synced'] == 2  # 111111 updated, 444444 updated + manifested
    assert stats['deleted'] == 1  # 222222 deleted
    assert stats['errors'] == 0
    assert stats['manifested'] == 1  # 444444 manifested

    # Verify database save was called
    suggestions_cog._save_suggestions_to_db.assert_called()

    # Verify channel creation was called
    suggestions_cog._create_suggested_channel.assert_called_once()


@pytest.mark.asyncio
async def test_sync_returns_empty_stats_for_no_suggestions_channel(suggestions_cog, mock_guild):
    """Test that sync returns empty stats if suggestions channel doesn't exist"""

    # Mock no suggestions channel
    suggestions_cog.get_suggestions_channel = Mock(return_value=None)

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Empty stats returned
    assert stats == {'synced': 0, 'deleted': 0, 'errors': 0, 'manifested': 0}


@pytest.mark.asyncio
async def test_sync_filters_by_guild(suggestions_cog, mock_guild, mock_suggestions_channel):
    """Test that sync only processes wishes for the specified guild"""

    # Setup: Wishes from different guilds
    mock_suggestions = {
        '111111': {
            'type': 'video',
            'guild_id': 987654321,  # Matches mock_guild
            'channel_id': 111222333,
            'votes': 5,
            'status': 'active',
            'description': 'Our guild wish'
        },
        '222222': {
            'type': 'video',
            'guild_id': 999999999,  # Different guild
            'channel_id': 111222333,
            'votes': 5,
            'status': 'active',
            'description': 'Other guild wish'
        }
    }

    # Mock message for our guild's wish
    mock_message = create_mock_message(111111, 8)
    mock_suggestions_channel.fetch_message = AsyncMock(return_value=mock_message)

    # Mock database methods
    suggestions_cog._load_suggestions = Mock(return_value=mock_suggestions.copy())
    suggestions_cog._save_suggestions_to_db = Mock()

    # Execute sync
    stats = await suggestions_cog.sync_reaction_counts(mock_guild)

    # Verify: Only our guild's wish was processed
    assert stats['synced'] == 1

    # Verify: Only one fetch_message call (for our guild)
    assert mock_suggestions_channel.fetch_message.call_count == 1
    mock_suggestions_channel.fetch_message.assert_called_with(111111)
