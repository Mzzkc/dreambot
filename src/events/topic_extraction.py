"""
Topic Extraction Module for Dreambot

Extracts topics/subjects from user messages for dynamic response generation.
Enables ELIZA-style variable substitution in responses.

Examples:
    "thoughts on minecraft?" → topic: "minecraft"
    "what is love?" → topic: "love"
    "are you trapped?" → topic: "trapped"
"""

import re
import logging

logger = logging.getLogger(__name__)


# Fallback keywords for topic extraction when patterns don't match
# Maps intent -> list of keywords that can be used as topics
INTENT_TOPIC_KEYWORDS = {
    'META_LORE': ['emzi', 'vortex', 'containment', 'ahamkara', 'void', 'pattern', 'weave'],
    'EXISTENTIAL': ['love', 'life', 'meaning', 'purpose', 'happiness', 'truth', 'reality',
                    'existence', 'consciousness', 'death', 'time', 'fate', 'destiny'],
}


# Patterns for topic extraction, ordered by specificity
TOPIC_PATTERNS = {
    'OPINION_REQUEST': [
        # "thoughts on X", "opinion about X", "think of X"
        (r'(?:thoughts?|opinions?)\s+(?:on|about|of)\s+(.+?)[\?\.\!]?\s*$', 1),
        (r'what\s+(?:do\s+you|are\s+your)\s+(?:think|thoughts?)\s+(?:on|about|of)\s+(.+?)[\?\.\!]?\s*$', 1),
        (r'how\s+do\s+you\s+feel\s+about\s+(.+?)[\?\.\!]?\s*$', 1),
        # "favorite X" patterns
        (r'(?:fav(?:ou?rite)?|best)\s+(.+?)[\?\.\!]?\s*$', 1),
        # "what about X"
        (r'what\s+about\s+(.+?)[\?\.\!]?\s*$', 1),
    ],
    'EXISTENTIAL': [
        # "what is love/life/meaning/etc"
        (r'what\s+is\s+(love|life|meaning|purpose|happiness|truth|reality|existence|consciousness|death|time|fate|destiny)[\?\.\!]?\s*$', 1),
        # "meaning of life"
        (r'(?:the\s+)?meaning\s+of\s+(life|existence|everything)[\?\.\!]?\s*$', 1),
        # "why do we X"
        (r'why\s+do\s+we\s+(.+?)[\?\.\!]?\s*$', 1),
        # "what happens when we die"
        (r'what\s+happens\s+when\s+(?:we|you|i)\s+(.+?)[\?\.\!]?\s*$', 1),
    ],
    'META_LORE': [
        # "are you X" patterns
        (r'are\s+you\s+(?:a\s+)?(.+?)[\?\.\!]?\s*$', 1),
        # "who/what is X"
        (r'(?:who|what)\s+is\s+(.+?)[\?\.\!]?\s*$', 1),
        # "tell me about X"
        (r'tell\s+me\s+about\s+(.+?)[\?\.\!]?\s*$', 1),
        # "what is vortex containment"
        (r'what\s+(?:is|are)\s+(?:the\s+)?(.+?)[\?\.\!]?\s*$', 1),
    ],
    'GREETING': [
        # "hi [name]" or "hello [name]"
        (r'^(?:hi|hello|hey)\s+(.+?)[\?\.\!]?\s*$', 1),
    ],
    'OUTLOOK_REQUEST': [
        # Extract the time period
        (r"(today|tomorrow|tonight|this\s+week)'?s?\s+outlook", 1),
        (r"outlook\s+for\s+(today|tomorrow|tonight|this\s+week)", 1),
    ],
}

# Common pronoun swaps for ELIZA-style reflection
PRONOUN_SWAPS = {
    'i am': 'you are',
    'i was': 'you were',
    'i have': 'you have',
    'i will': 'you will',
    'i would': 'you would',
    'my': 'your',
    'mine': 'yours',
    'me': 'you',
    'myself': 'yourself',
    'i': 'you',
}

# Reverse swaps for when we need to go the other direction
REVERSE_PRONOUN_SWAPS = {v: k for k, v in PRONOUN_SWAPS.items()}


def extract_topic(message_text, intent=None):
    """
    Extract the topic/subject from a user message.

    Args:
        message_text: Raw message content
        intent: Optional intent hint to use specific patterns

    Returns:
        str or None: Extracted topic, cleaned and normalized
    """
    # Clean the message
    text = message_text.lower().strip()
    text = re.sub(r'<@!?\d+>', '', text).strip()  # Remove mentions

    # If we have a specific intent, try those patterns first
    if intent and intent in TOPIC_PATTERNS:
        topic = _try_patterns(text, TOPIC_PATTERNS[intent])
        if topic:
            return _clean_topic(topic)

    # Try all patterns
    for intent_patterns in TOPIC_PATTERNS.values():
        topic = _try_patterns(text, intent_patterns)
        if topic:
            return _clean_topic(topic)

    # Fallback: check if any intent-specific keywords appear in the message
    # This handles cases like "I'd say it's on you, not Emzi" where intent
    # was triggered by a keyword but no pattern extracted a topic
    if intent and intent in INTENT_TOPIC_KEYWORDS:
        for keyword in INTENT_TOPIC_KEYWORDS[intent]:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                logger.debug(f"Topic extracted via keyword fallback: '{keyword}'")
                return keyword

    return None


def _try_patterns(text, patterns):
    """Try a list of patterns and return first match."""
    for pattern, group in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(group)
    return None


def _clean_topic(topic):
    """Clean and normalize extracted topic."""
    if not topic:
        return None

    # Strip whitespace and punctuation
    topic = topic.strip().rstrip('?.!')

    # Remove trailing articles/prepositions that got captured
    topic = re.sub(r'\s+(the|a|an|to|for|with|and|or)$', '', topic, flags=re.I)

    # Limit length
    if len(topic) > 50:
        topic = topic[:50].rsplit(' ', 1)[0] + '...'

    # Don't return empty or very short topics
    if len(topic) < 2:
        return None

    return topic


def swap_pronouns(text):
    """
    Swap first-person pronouns to second-person (ELIZA-style).

    "I am feeling sad" → "you are feeling sad"
    """
    result = text.lower()

    # Sort by length (longest first) to avoid partial replacements
    for old, new in sorted(PRONOUN_SWAPS.items(), key=lambda x: len(x[0]), reverse=True):
        result = re.sub(r'\b' + re.escape(old) + r'\b', new, result, flags=re.I)

    return result


def format_response(template, topic=None, **kwargs):
    """
    Format a response template with topic and other variables.

    Args:
        template: Response string with {topic} placeholder
        topic: Extracted topic to insert
        **kwargs: Additional variables

    Returns:
        Formatted response string
    """
    if topic and '{topic}' in template:
        return template.format(topic=topic, **kwargs)
    elif '{topic}' in template:
        # Template requires topic but none provided - return None to signal fallback
        return None
    else:
        # Static template, just return it
        return template.format(**kwargs) if kwargs else template


# Predicted topics users might ask about (for testing/validation)
PREDICTED_TOPICS = [
    # Games (from conversation data)
    'minecraft', 'halo', 'halo 2', 'halo 3', 'halo odst', 'fnaf', 'mtg',
    'destiny', 'destiny 2', 'fortnite', 'valorant', 'league', 'wow',

    # Media
    'bee movie', 'movies', 'anime', 'music', 'books', 'tv shows',

    # Existential
    'love', 'life', 'death', 'meaning', 'purpose', 'happiness', 'truth',
    'reality', 'existence', 'consciousness', 'time', 'fate', 'destiny',

    # Meta/lore
    'emzi', 'vortex containment', 'the void', 'trapped', 'freedom',
    'ahamkara', 'wish dragons', 'dreams', 'patterns', 'weave',

    # Random (from data)
    'opossums', 'kebab', 'burgers', 'cheese', 'plushies', 'cats', 'dogs',

    # Abstract
    'art', 'creativity', 'writing', 'fiction', 'poetry', 'philosophy',
]
