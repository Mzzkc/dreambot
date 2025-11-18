import discord
from discord.ext import commands
import random
import re
from utils import zalgo_text
from config import AHAMKARA_8BALL, VAGUE_STATEMENTS
from database import load_8ball_usage, increment_8ball_usage, load_vague_usage, increment_vague_usage


def is_question(text):
    """
    Detect if a message is a question.

    Checks for:
    - Contains '?'
    - Modal question patterns (will/would/should/could/can/is/are/do + subject)
    """
    text_lower = text.lower().strip()

    # Remove bot mention for analysis
    text_clean = re.sub(r'<@!?\d+>', '', text_lower).strip()

    # Explicit question mark - strongest signal
    if '?' in text_clean:
        return True

    # Modal questions (will/would/should/could/can + subject)
    # Examples: "will you", "should i", "can this", "is it"
    modal_patterns = [
        r'^(will|would|should|could|can|may|might|shall|must)\s+\w+',
        r'^(is|are|was|were|am|has|have|had|do|does|did)\s+\w+',
    ]
    for pattern in modal_patterns:
        if re.match(pattern, text_clean):
            return True

    return False


def select_weighted_8ball():
    """Select a magic 8-ball response using weighted randomness (ID-based)."""
    usage_data = load_8ball_usage()

    # Calculate weights based on ID usage
    weights = []
    for response in AHAMKARA_8BALL:
        response_id = response["id"]
        usage_count = usage_data.get(response_id, {}).get('usage_count', 0)
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    # Select response object and increment
    selected = random.choices(AHAMKARA_8BALL, weights=weights, k=1)[0]
    increment_8ball_usage(selected["id"], selected["text"])

    # Return just the text for display
    return selected["text"]


def select_weighted_vague():
    """Select a vague statement using weighted randomness (ID-based)."""
    usage_data = load_vague_usage()

    # Calculate weights based on ID usage
    weights = []
    for statement in VAGUE_STATEMENTS:
        statement_id = statement["id"]
        usage_count = usage_data.get(statement_id, {}).get('usage_count', 0)
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    # Select statement object and increment
    selected = random.choices(VAGUE_STATEMENTS, weights=weights, k=1)[0]
    increment_vague_usage(selected["id"], selected["text"])

    # Return just the text for display
    return selected["text"]


class MessageEvents(commands.Cog):
    """Handle message-related events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Respond when bot is tagged - magic 8-ball for questions, vague for statements"""
        # Ignore own messages
        if message.author == self.bot.user:
            return

        # Check if bot was mentioned
        if self.bot.user in message.mentions:
            # Determine response type based on question detection
            if is_question(message.content):
                # Magic 8-ball response for questions
                response = select_weighted_8ball()
            else:
                # Vague indescipherable statement for non-questions
                response = select_weighted_vague()

            # Apply extreme zalgo for full eldritch effect
            zalgo_response = zalgo_text(response, intensity='extreme')

            # Send as italicized plain text
            await message.channel.send(f"*{zalgo_response}*")


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
