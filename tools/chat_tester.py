#!/usr/bin/env python3
"""
Dreambot Chat Tester - Interactive shell for testing response system

Usage: python tools/chat_tester.py

Commands:
    /debug      Toggle debug output (shows intent, topic, pool)
    /zalgo      Toggle zalgo text transformation
    /stats [pool]  Show usage statistics for a pool
    /reset      Clear conversation context for current user
    /user <id>  Change simulated user ID
    /help       Show this help message
    /quit       Exit the tester
"""

import sys
import os
import random
import re

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Ensure we use JSON fallback (no Supabase)
os.environ.pop('SUPABASE_URL', None)
os.environ.pop('SUPABASE_KEY', None)

# Import from existing codebase
from events.intent_detection import detect_intent
from events.topic_extraction import extract_topic, format_response
from events.conversation_context import (
    record_message,
    get_joke_intensity,
    detect_repetition,
    should_lore_callback,
    record_message_timestamp,
    is_escaped,
    should_trigger_escape,
    trigger_escape,
    conversation_context,
)
from database import (
    load_pool_usage,
    increment_pool_usage,
    load_8ball_usage,
    increment_8ball_usage,
    load_vague_usage,
    increment_vague_usage,
)
from config.constants import (
    AHAMKARA_8BALL,
    VAGUE_STATEMENTS,
    GREETING_RESPONSES,
    GRATITUDE_RESPONSES,
    KEBAB_RESPONSES,
    OUTLOOK_RESPONSES,
    OPINION_RESPONSES,
    OPINION_DYNAMIC_RESPONSES,
    FAREWELL_RESPONSES,
    EXISTENTIAL_RESPONSES,
    META_LORE_RESPONSES,
    CHALLENGE_RESPONSES,
    ANIMAL_SOUND_RESPONSES,
    SIMPLE_AFFIRMATION_RESPONSES,
    SIMPLE_NEGATION_RESPONSES,
    SIMPLE_EXCLAMATION_RESPONSES,
    SELF_STATEMENT_RESPONSES,
    BOT_CAPABILITY_RESPONSES,
    IMPERATIVE_RESPONSES,
    SHARING_RESPONSES,
    EMOTIONAL_REACTION_RESPONSES,
    ROLEPLAY_INVITATION_RESPONSES,
    CORRECTION_RESPONSES,
    CONFUSION_RESPONSES,
    KEBAB_INTENSE_RESPONSES,
    REPETITION_META_RESPONSES,
    LORE_CALLBACK_RESPONSES,
    ESCAPE_RESPONSES,
)
from utils import zalgo_text

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_USER_ID = 12345
KEBAB_INTENSE_THRESHOLD = 3

# Global state
debug_mode = False
zalgo_enabled = True
current_user_id = DEFAULT_USER_ID

# =============================================================================
# Intent to Pool Mapping (copied from message_events.py)
# =============================================================================

INTENT_POOL_MAP = {
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
    'SELF_STATEMENT': ('self_statement', SELF_STATEMENT_RESPONSES, False),
    'BOT_CAPABILITY': ('bot_capability', BOT_CAPABILITY_RESPONSES, False),
    'IMPERATIVE': ('imperative', IMPERATIVE_RESPONSES, False),
    'SHARING': ('sharing', SHARING_RESPONSES, False),
    'EMOTIONAL_REACTION': ('emotional', EMOTIONAL_REACTION_RESPONSES, False),
    'ROLEPLAY_INVITATION': ('roleplay', ROLEPLAY_INVITATION_RESPONSES, False),
    'CORRECTION': ('correction', CORRECTION_RESPONSES, False),
    'CONFUSION': ('confusion', CONFUSION_RESPONSES, False),
}

CONTEXT_POOLS = {
    'KEBAB_INTENSE': ('kebab_intense', KEBAB_INTENSE_RESPONSES),
    'REPETITION_META': ('repetition', REPETITION_META_RESPONSES),
    'LORE_CALLBACK': ('lore_callback', LORE_CALLBACK_RESPONSES),
    'ESCAPE': ('escape', ESCAPE_RESPONSES),
}

# =============================================================================
# Helper Functions (adapted from message_events.py)
# =============================================================================

def is_question(text: str) -> bool:
    """Detect if a message is a question."""
    text_lower = text.lower().strip()

    if '?' in text_lower:
        return True

    modal_patterns = [
        r'^(will|would|should|could|can|may|might|shall|must)\s+\w+',
        r'^(is|are|was|were|am|has|have|had|do|does|did)\s+\w+',
    ]
    for pattern in modal_patterns:
        if re.match(pattern, text_lower):
            return True

    return False


def select_weighted_8ball() -> str:
    """Select a magic 8-ball response using weighted randomness."""
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


def select_weighted_vague() -> str:
    """Select a vague statement using weighted randomness."""
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


def select_weighted_pool_response(pool_name: str, response_pool: list, topic: str = None) -> str:
    """Generic weighted response selector with dynamic template support."""
    usage_data = load_pool_usage(pool_name)

    candidates = response_pool

    if topic:
        template_responses = [r for r in response_pool if '{topic}' in r['text']]
        if template_responses:
            candidates = template_responses

    weights = []
    for response in candidates:
        response_id = response["id"]
        usage_count = usage_data.get(response_id, {}).get('usage_count', 0)
        weight = 1.0 / ((usage_count + 1) ** 2)
        weights.append(weight)

    selected = random.choices(candidates, weights=weights, k=1)[0]

    response_text = selected["text"]
    if topic and '{topic}' in response_text:
        response_text = format_response(response_text, topic=topic)

    increment_pool_usage(pool_name, selected["id"], selected["text"])

    return response_text


# =============================================================================
# Main Processing
# =============================================================================

def process_message(user_id: int, message: str) -> tuple:
    """
    Process a message and return (response, debug_info).

    Returns:
        tuple: (response_text, debug_info_dict)
    """
    debug_info = {
        'intent': None,
        'topic': None,
        'pool': None,
        'context_used': None,
        'escaped': False,
    }

    # Step 0: Escape path handling
    record_message_timestamp(user_id)

    if is_escaped(user_id):
        debug_info['escaped'] = True
        return None, debug_info

    if should_trigger_escape(user_id):
        pool_name, response_pool = CONTEXT_POOLS['ESCAPE']
        escape_response = select_weighted_pool_response(pool_name, response_pool)
        trigger_escape(user_id)
        debug_info['pool'] = 'escape'
        debug_info['context_used'] = 'ESCAPE_TRIGGERED'

        if zalgo_enabled:
            zalgo_response = zalgo_text(escape_response, intensity='extreme')
            return f"*{zalgo_response}*", debug_info
        else:
            return escape_response, debug_info

    # Step 1: Detect intent
    is_question_flag = is_question(message)
    intent = detect_intent(message, is_question_flag)
    debug_info['intent'] = intent

    # Step 2: Extract topic
    topic = None
    if intent:
        topic = extract_topic(message, intent)
        debug_info['topic'] = topic

    # Step 3: Context-aware response selection
    response = None
    used_context = False

    # Check for kebab intensity
    if intent == 'KEBAB':
        kebab_intensity = get_joke_intensity(user_id, 'kebab')
        if kebab_intensity >= KEBAB_INTENSE_THRESHOLD:
            pool_name, response_pool = CONTEXT_POOLS['KEBAB_INTENSE']
            response = select_weighted_pool_response(pool_name, response_pool)
            debug_info['pool'] = 'kebab_intense'
            debug_info['context_used'] = f'KEBAB_INTENSITY={kebab_intensity}'
            used_context = True

    # Check for repetition
    if not response and detect_repetition(user_id, intent, topic):
        pool_name, response_pool = CONTEXT_POOLS['REPETITION_META']
        response = select_weighted_pool_response(pool_name, response_pool)
        debug_info['pool'] = 'repetition'
        debug_info['context_used'] = 'REPETITION_DETECTED'
        used_context = True

    # Standard intent-based selection
    if not response:
        if intent and intent in INTENT_POOL_MAP:
            pool_name, response_pool, supports_topic = INTENT_POOL_MAP[intent]

            if supports_topic and topic:
                response = select_weighted_pool_response(pool_name, response_pool, topic=topic)
            else:
                response = select_weighted_pool_response(pool_name, response_pool)

            debug_info['pool'] = pool_name
        else:
            # Fallback to 8-ball or vague
            if is_question_flag:
                response = select_weighted_8ball()
                debug_info['pool'] = '8ball (fallback)'
            else:
                response = select_weighted_vague()
                debug_info['pool'] = 'vague (fallback)'

    # Step 4: Lore callback check
    lore_suffix = None
    if should_lore_callback(user_id) and not used_context:
        pool_name, response_pool = CONTEXT_POOLS['LORE_CALLBACK']
        lore_suffix = select_weighted_pool_response(pool_name, response_pool)
        debug_info['context_used'] = 'LORE_CALLBACK'

    # Step 5: Record message in context
    record_message(user_id, message, intent, topic, response)

    # Step 6: Format response
    if lore_suffix:
        full_response = f"{response}\n\n{lore_suffix}"
    else:
        full_response = response

    if zalgo_enabled:
        zalgo_response = zalgo_text(full_response, intensity='extreme')
        return f"*{zalgo_response}*", debug_info
    else:
        return full_response, debug_info


# =============================================================================
# Commands
# =============================================================================

def show_help():
    """Display help message."""
    print("""
Commands:
  /debug       Toggle debug output (shows intent, topic, pool)
  /zalgo       Toggle zalgo text transformation
  /stats [pool]  Show usage statistics (pools: 8ball, vague, greeting, etc.)
  /reset       Clear conversation context for current user
  /user <id>   Change simulated user ID (current: {})
  /help        Show this help message
  /quit        Exit the tester

Just type a message to chat with Dreambot!
""".format(current_user_id))


def show_stats(pool_name: str = None):
    """Show usage statistics for a pool."""
    if not pool_name:
        print("Available pools: 8ball, vague, greeting, gratitude, kebab, outlook,")
        print("  opinion, farewell, existential, meta_lore, challenge, animal_sound,")
        print("  affirmation, negation, exclamation, self_statement, bot_capability,")
        print("  imperative, sharing, emotional, roleplay, correction, confusion,")
        print("  kebab_intense, repetition, lore_callback, escape")
        return

    pool_name = pool_name.lower()

    if pool_name == '8ball':
        usage_data = load_8ball_usage()
        pool_responses = AHAMKARA_8BALL
    elif pool_name == 'vague':
        usage_data = load_vague_usage()
        pool_responses = VAGUE_STATEMENTS
    else:
        usage_data = load_pool_usage(pool_name)
        # Find the pool
        pool_responses = None
        for intent, (pname, responses, _) in INTENT_POOL_MAP.items():
            if pname == pool_name:
                pool_responses = responses
                break
        if not pool_responses:
            for context, (pname, responses) in CONTEXT_POOLS.items():
                if pname == pool_name:
                    pool_responses = responses
                    break

    if not pool_responses:
        print(f"Unknown pool: {pool_name}")
        return

    print(f"\nPool: {pool_name} ({len(pool_responses)} responses)")
    print("-" * 40)

    if not usage_data:
        print("No usage data yet.")
        return

    # Sort by usage count
    sorted_usage = sorted(usage_data.items(), key=lambda x: x[1].get('usage_count', 0), reverse=True)

    for response_id, stats in sorted_usage[:15]:  # Show top 15
        count = stats.get('usage_count', 0)
        text_preview = stats.get('text', '')[:40]
        print(f"  {response_id}: {count} uses - \"{text_preview}...\"")

    if len(sorted_usage) > 15:
        print(f"  ... and {len(sorted_usage) - 15} more")


def reset_context():
    """Reset conversation context for current user."""
    global current_user_id
    if current_user_id in conversation_context._users:
        del conversation_context._users[current_user_id]
        print(f"Context cleared for user {current_user_id}")
    else:
        print(f"No context to clear for user {current_user_id}")


def handle_command(cmd: str) -> bool:
    """
    Handle a slash command.

    Returns:
        bool: True if should continue, False if should exit
    """
    global debug_mode, zalgo_enabled, current_user_id

    parts = cmd.split()
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []

    if command == '/quit' or command == '/exit':
        return False

    elif command == '/help':
        show_help()

    elif command == '/debug':
        debug_mode = not debug_mode
        print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")

    elif command == '/zalgo':
        zalgo_enabled = not zalgo_enabled
        print(f"Zalgo mode: {'ON' if zalgo_enabled else 'OFF'}")

    elif command == '/stats':
        pool_name = args[0] if args else None
        show_stats(pool_name)

    elif command == '/reset':
        reset_context()

    elif command == '/user':
        if args:
            try:
                current_user_id = int(args[0])
                print(f"Switched to user ID: {current_user_id}")
            except ValueError:
                print("Invalid user ID. Must be a number.")
        else:
            print(f"Current user ID: {current_user_id}")

    else:
        print(f"Unknown command: {command}")
        print("Type /help for available commands.")

    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Main REPL loop."""
    global current_user_id

    print("=" * 50)
    print("  Dreambot Chat Tester")
    print("  Type /help for commands, or just chat!")
    print("=" * 50)

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            if user_input.startswith('/'):
                if not handle_command(user_input):
                    print("\nGoodbye, O Bearer Mine...")
                    break
            else:
                response, debug_info = process_message(current_user_id, user_input)

                if debug_mode:
                    print(f"[Intent: {debug_info['intent']}]")
                    print(f"[Topic: {debug_info['topic']}]")
                    print(f"[Pool: {debug_info['pool']}]")
                    if debug_info['context_used']:
                        print(f"[Context: {debug_info['context_used']}]")

                if response is None:
                    if debug_info['escaped']:
                        print("(User is escaped - bot is ignoring)")
                else:
                    print(f"\n{response}")

        except KeyboardInterrupt:
            print("\n\nGoodbye, O Bearer Mine...")
            break
        except EOFError:
            print("\n\nGoodbye, O Bearer Mine...")
            break


if __name__ == "__main__":
    main()
