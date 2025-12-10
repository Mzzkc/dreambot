import discord
from discord.ext import commands
import random
import re
import logging
from utils import zalgo_text
from config import (
    AHAMKARA_8BALL,
    VAGUE_STATEMENTS,
    # Phase 1 pools
    GREETING_RESPONSES,
    GRATITUDE_RESPONSES,
    KEBAB_RESPONSES,
    OUTLOOK_RESPONSES,
    OPINION_RESPONSES,
    FAREWELL_RESPONSES,
    OPINION_DYNAMIC_RESPONSES,
    EXISTENTIAL_RESPONSES,
    META_LORE_RESPONSES,
    CHALLENGE_RESPONSES,
    ANIMAL_SOUND_RESPONSES,
    SIMPLE_AFFIRMATION_RESPONSES,
    SIMPLE_NEGATION_RESPONSES,
    SIMPLE_EXCLAMATION_RESPONSES,
    # Phase 2 pools
    SELF_STATEMENT_RESPONSES,
    BOT_CAPABILITY_RESPONSES,
    IMPERATIVE_RESPONSES,
    SHARING_RESPONSES,
    EMOTIONAL_REACTION_RESPONSES,
    ROLEPLAY_INVITATION_RESPONSES,
    CORRECTION_RESPONSES,
    CONFUSION_RESPONSES,
    # Phase 3 context-aware pools
    KEBAB_INTENSE_RESPONSES,
    REPETITION_META_RESPONSES,
    LORE_CALLBACK_RESPONSES,
    # Escape path pool
    ESCAPE_RESPONSES,
)
from database import (
    load_8ball_usage,
    increment_8ball_usage,
    load_vague_usage,
    increment_vague_usage,
    load_pool_usage,
    increment_pool_usage,
)
from events.intent_detection import detect_intent
from events.topic_extraction import extract_topic, format_response
from events.conversation_context import (
    record_message,
    get_joke_intensity,
    detect_repetition,
    should_lore_callback,
    # Escape path functions
    record_message_timestamp,
    is_escaped,
    should_trigger_escape,
    trigger_escape,
)

# Kebab intensity threshold for using intense responses
KEBAB_INTENSE_THRESHOLD = 3

logger = logging.getLogger(__name__)


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

    weights = []
    for response in AHAMKARA_8BALL:
        response_id = response["id"]
        usage_count = usage_data.get(response_id, {}).get('usage_count', 0)
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    selected = random.choices(AHAMKARA_8BALL, weights=weights, k=1)[0]
    increment_8ball_usage(selected["id"], selected["text"])

    return selected["text"]


def select_weighted_vague():
    """Select a vague statement using weighted randomness (ID-based)."""
    usage_data = load_vague_usage()

    weights = []
    for statement in VAGUE_STATEMENTS:
        statement_id = statement["id"]
        usage_count = usage_data.get(statement_id, {}).get('usage_count', 0)
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    selected = random.choices(VAGUE_STATEMENTS, weights=weights, k=1)[0]
    increment_vague_usage(selected["id"], selected["text"])

    return selected["text"]


def select_weighted_pool_response(pool_name, response_pool, topic=None):
    """
    Generic weighted response selector with dynamic template support.

    Args:
        pool_name: String identifier for the pool (e.g., 'greeting', 'kebab')
        response_pool: List of response dicts with 'id' and 'text' keys
        topic: Optional extracted topic for template responses

    Returns:
        str: Selected and formatted response text
    """
    usage_data = load_pool_usage(pool_name)

    # If we have a topic, filter to only template responses first
    # If that fails or no topic, use all responses
    candidates = response_pool

    if topic:
        # Try to find responses that can use the topic
        template_responses = [r for r in response_pool if '{topic}' in r['text']]
        if template_responses:
            candidates = template_responses

    # Calculate weights
    weights = []
    for response in candidates:
        response_id = response["id"]
        usage_count = usage_data.get(response_id, {}).get('usage_count', 0)
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    # Select response
    selected = random.choices(candidates, weights=weights, k=1)[0]

    # Format with topic if applicable
    response_text = selected["text"]
    if topic and '{topic}' in response_text:
        response_text = format_response(response_text, topic=topic)

    # Increment usage with the TEMPLATE (not the formatted text)
    increment_pool_usage(pool_name, selected["id"], selected["text"])

    return response_text


# Intent to response pool mapping
# Maps intent names to (pool_name, response_pool, supports_topic) tuples
INTENT_POOL_MAP = {
    # =========================================================================
    # PHASE 1 - Core intents
    # =========================================================================
    'GREETING': ('greeting', GREETING_RESPONSES, False),
    'GRATITUDE': ('gratitude', GRATITUDE_RESPONSES, False),
    'KEBAB': ('kebab', KEBAB_RESPONSES, False),
    'OUTLOOK_REQUEST': ('outlook', OUTLOOK_RESPONSES, False),
    'FAREWELL': ('farewell', FAREWELL_RESPONSES, False),
    'OPINION_REQUEST': ('opinion', OPINION_RESPONSES + OPINION_DYNAMIC_RESPONSES, True),
    'EXISTENTIAL': ('existential', EXISTENTIAL_RESPONSES, True),
    'META_LORE': ('meta_lore', META_LORE_RESPONSES, True),
    'CHALLENGE': ('challenge', CHALLENGE_RESPONSES, False),
    'ANIMAL_SOUND': ('animal_sound', ANIMAL_SOUND_RESPONSES, False),
    'SIMPLE_AFFIRMATION': ('affirmation', SIMPLE_AFFIRMATION_RESPONSES, False),
    'SIMPLE_NEGATION': ('negation', SIMPLE_NEGATION_RESPONSES, False),
    'SIMPLE_EXCLAMATION': ('exclamation', SIMPLE_EXCLAMATION_RESPONSES, False),

    # =========================================================================
    # PHASE 2 - Expanded coverage
    # =========================================================================
    'SELF_STATEMENT': ('self_statement', SELF_STATEMENT_RESPONSES, False),
    'BOT_CAPABILITY': ('bot_capability', BOT_CAPABILITY_RESPONSES, False),
    'IMPERATIVE': ('imperative', IMPERATIVE_RESPONSES, False),
    'SHARING': ('sharing', SHARING_RESPONSES, False),
    'EMOTIONAL_REACTION': ('emotional', EMOTIONAL_REACTION_RESPONSES, False),
    'ROLEPLAY_INVITATION': ('roleplay', ROLEPLAY_INVITATION_RESPONSES, False),
    'CORRECTION': ('correction', CORRECTION_RESPONSES, False),
    'CONFUSION': ('confusion', CONFUSION_RESPONSES, False),
}

# Phase 3 context-aware pools (not in main map - selected dynamically)
CONTEXT_POOLS = {
    'KEBAB_INTENSE': ('kebab_intense', KEBAB_INTENSE_RESPONSES),
    'REPETITION_META': ('repetition', REPETITION_META_RESPONSES),
    'LORE_CALLBACK': ('lore_callback', LORE_CALLBACK_RESPONSES),
    'ESCAPE': ('escape', ESCAPE_RESPONSES),
}


class MessageEvents(commands.Cog):
    """Handle message-related events"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Respond when bot is tagged - context-aware intent-based response selection"""
        # Ignore own messages
        if message.author == self.bot.user:
            return

        # Check if bot was mentioned
        if self.bot.user in message.mentions:
            user_id = message.author.id

            # Step 0: Escape path handling
            # Record timestamp for rate detection (must happen before escape check)
            record_message_timestamp(user_id)

            # Check if user is currently escaped - silently ignore
            if is_escaped(user_id):
                logger.debug(f"[Escape] User {user_id} is escaped, ignoring message")
                return

            # Check if escape should trigger based on message rate
            if should_trigger_escape(user_id):
                # Send escape message and trigger escape
                pool_name, response_pool = CONTEXT_POOLS['ESCAPE']
                escape_response = select_weighted_pool_response(pool_name, response_pool)
                trigger_escape(user_id)
                logger.info(f"[Escape] Triggered for user {user_id}")

                # Send escape message with zalgo
                zalgo_response = zalgo_text(escape_response, intensity='extreme')
                await message.channel.send(f"*{zalgo_response}*")
                return

            # Step 1: Detect if question (for fallback logic)
            is_question_flag = is_question(message.content)

            # Step 2: Detect intent
            intent = detect_intent(message.content, is_question_flag)

            # Step 3: Extract topic if applicable
            topic = None
            if intent:
                topic = extract_topic(message.content, intent)
                if topic:
                    logger.info(f"[Topic] Extracted '{topic}' from message")

            # Step 4: Context-aware response selection
            response = None
            used_context = False

            # Check for kebab intensity (running joke escalation)
            if intent == 'KEBAB':
                kebab_intensity = get_joke_intensity(user_id, 'kebab')
                if kebab_intensity >= KEBAB_INTENSE_THRESHOLD:
                    pool_name, response_pool = CONTEXT_POOLS['KEBAB_INTENSE']
                    response = select_weighted_pool_response(pool_name, response_pool)
                    logger.info(f"[Context] Kebab intensity {kebab_intensity} -> KEBAB_INTENSE")
                    used_context = True

            # Check for repetition (same question asked before)
            if not response and detect_repetition(user_id, intent, topic):
                pool_name, response_pool = CONTEXT_POOLS['REPETITION_META']
                response = select_weighted_pool_response(pool_name, response_pool)
                logger.info(f"[Context] Repetition detected for intent '{intent}'")
                used_context = True

            # Standard intent-based selection
            if not response:
                if intent and intent in INTENT_POOL_MAP:
                    pool_name, response_pool, supports_topic = INTENT_POOL_MAP[intent]

                    # Pass topic only if this pool supports it
                    if supports_topic and topic:
                        response = select_weighted_pool_response(pool_name, response_pool, topic=topic)
                        logger.info(f"[Intent] Matched '{intent}' with topic '{topic}'")
                    else:
                        response = select_weighted_pool_response(pool_name, response_pool)
                        logger.info(f"[Intent] Matched '{intent}' (no topic)")
                else:
                    # Fallback to default question/statement pools
                    if is_question_flag:
                        response = select_weighted_8ball()
                        logger.debug(f"[Intent] Fallback to 8ball (question)")
                    else:
                        response = select_weighted_vague()
                        logger.debug(f"[Intent] Fallback to vague (statement)")

            # Step 5: Check for lore callback opportunity (append to response)
            lore_suffix = None
            if should_lore_callback(user_id) and not used_context:
                pool_name, response_pool = CONTEXT_POOLS['LORE_CALLBACK']
                lore_suffix = select_weighted_pool_response(pool_name, response_pool)
                logger.info(f"[Context] Lore callback triggered")

            # Step 6: Record message in context
            record_message(user_id, message.content, intent, topic, response)

            # Step 7: Apply zalgo and send
            if lore_suffix:
                # Combine main response with lore callback
                full_response = f"{response}\n\n{lore_suffix}"
                zalgo_response = zalgo_text(full_response, intensity='extreme')
            else:
                zalgo_response = zalgo_text(response, intensity='extreme')

            # Send as italicized plain text
            await message.channel.send(f"*{zalgo_response}*")


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
