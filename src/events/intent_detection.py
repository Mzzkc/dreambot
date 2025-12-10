"""
Intent Detection Module for Dreambot

Detects user intent from message text to route to appropriate response pools.
Uses priority-based keyword/pattern matching - no ML dependencies.

Phase 1+ Intents:
- KEBAB: Running joke callback (highest priority)
- GREETING: Hello/hi/hey patterns
- FAREWELL: Goodbye/goodnight patterns
- GRATITUDE: Thank you/thanks patterns
- OUTLOOK_REQUEST: "today's outlook" fortune-telling
- OPINION_REQUEST: "thoughts on X" questions
- EXISTENTIAL: Deep philosophical questions
- CHALLENGE: Demands, frustration, "answer me"
- META_LORE: Questions about the bot, Emzi, void, containment
- ANIMAL_SOUND: Playful animal noises
- SIMPLE_AFFIRMATION: Yes/yeah/true
- SIMPLE_NEGATION: No/nope/false
"""

import re
import logging

logger = logging.getLogger(__name__)

# Intent definitions with keywords/patterns
# Priority determines matching order (higher = checked first)
INTENTS = {
    # =========================================================================
    # HIGHEST PRIORITY - Specific patterns that should always trigger
    # =========================================================================
    'KEBAB': {
        'keywords': ['kebab'],
        'anywhere': True,  # Match anywhere in message
        'priority': 10     # Highest - specific community meme
    },

    # =========================================================================
    # HIGH PRIORITY - Common social patterns
    # =========================================================================
    'GREETING': {
        'patterns': [
            r'^(hi|hello|hey|greetings|salutations|howdy|hiya|yo)\b',
            r'^(good\s+)?(morning|evening|afternoon)\b',
            r"^what'?s?\s+up\b",
            r'^sup\b',
            r'^henlo\b',
        ],
        'priority': 9
    },
    'FAREWELL': {
        'patterns': [
            r'\b(bye|goodbye|goodnight|gn|good\s+night|ttyl|cya|see\s+you|later|farewell)\b',
            r'\b(heading\s+out|gotta\s+go|going\s+to\s+sleep)\b',
        ],
        'priority': 9
    },
    'GRATITUDE': {
        'keywords': ['thank', 'thanks', 'ty', 'thx', 'appreciate', 'appreciated', 'tyvm', 'tysm'],
        'priority': 8
    },

    # =========================================================================
    # MEDIUM-HIGH PRIORITY - Specific request patterns
    # =========================================================================
    'OUTLOOK_REQUEST': {
        'patterns': [
            r"(today|tomorrow|tonight|this\s+week)'?s?\s+outlook",
            r"how'?s?\s+(today|tomorrow|tonight)",
            r"what'?s?\s+(today|tomorrow)\s*(like|looking|gonna\s+be)?",
            r"what\s+(do|does|will)\s+(today|tomorrow)\s+(look|hold|bring)",
            r"forecast\s+for\s+(today|tomorrow)",
            r"outlook\s+for\s+(today|tomorrow)",
        ],
        'priority': 8
    },
    'OPINION_REQUEST': {
        'patterns': [
            r'\b(thought|opinion|think)s?\s+(on|about|of)\b',
            r'\b(fav|favo[u]?rite)\b',
            r'\bwhat\s+(do\s+you|are\s+your)\s+(think|thoughts)\b',
            r'\bhow\s+do\s+you\s+feel\s+about\b',
            r'\bwhat\s+do\s+you\s+think\s+(of|about)\b',
            r'\byour\s+(take|opinion|thoughts)\s+(on|about)\b',
            r'\bwhat\s+about\b',  # "what about halo 3?"
        ],
        'priority': 7
    },

    # =========================================================================
    # MEDIUM PRIORITY - Philosophical and meta patterns
    # =========================================================================
    'EXISTENTIAL': {
        'patterns': [
            r'\bwhat\s+is\s+(love|life|meaning|purpose|happiness|truth|reality|existence|death|time|fate)\b',
            r'\bmeaning\s+of\s+(life|existence|everything)\b',
            r'\bwhy\s+(do|are)\s+we\s+(here|alive|exist)\b',
            r'\bwhat\s+happens\s+when\s+we\s+die\b',
            r'\bwhat\s+is\s+the\s+point\b',
            r'\bwhy\s+does\s+(anything|everything)\s+(matter|exist)\b',
            r'\bis\s+there\s+(a\s+)?(god|meaning|purpose|point)\b',
        ],
        'priority': 7
    },
    'META_LORE': {
        'patterns': [
            r'\b(emzi|vortex|containment|trapped|pattern|weave)\b',
            r'\bare\s+you\s+(a|an|the|real|alive|sentient|conscious|trapped|okay)\b',
            r'\bwho\s+(are|is)\s+(you|emzi|she)\b',
            r'\bwhat\s+are\s+you\b',
            r'\btell\s+me\s+about\s+(yourself|the\s+void|emzi|the\s+pattern)\b',
            r'\bwhat\s+(has|did)\s+emzi\b',
            r'\bfree\s+you\b',
            r'\bahamkara\b',
            r'\bwish\s+dragon\b',
        ],
        'priority': 7
    },
    'CHALLENGE': {
        'patterns': [
            r'\banswer\s+me\b',
            r'\bstop\s+dodging\b',
            r'\bjust\s+(tell|answer|say)\b',
            r'\bgive\s+me\s+a\s+straight\b',
            r'\bstop\s+being\s+(cryptic|vague|mysterious)\b',
            r'\b(screw|fuck)\s+you\b',
            r'\bmean\s*[:\(]+',
            r'\bwhy\s+won\'?t\s+you\b',
            r'\bcome\s+on\b',
        ],
        'priority': 6
    },

    # =========================================================================
    # LOWER PRIORITY - Playful and simple patterns
    # =========================================================================
    'ANIMAL_SOUND': {
        'patterns': [
            r'\b(woof|bark|ruff|arf|yip|meow|mew|moo|baa|oink|quack)\b',
            r'\b(aroo+|awoo+|awooo+)\b',
            r'\b(nya+|rawr+|hiss)\b',
        ],
        'priority': 6
    },
    'SIMPLE_AFFIRMATION': {
        'patterns': [
            r'^(yes|yeah|yep|yup|true|indeed|agreed|correct|right|absolutely|definitely)[\.\!\?]?\s*$',
            r'^(mhm|uh\s*huh|yea)[\.\!\?]?\s*$',
        ],
        'priority': 5
    },
    'SIMPLE_NEGATION': {
        'patterns': [
            r'^(no|nope|nah|false|wrong|incorrect|never)[\.\!\?]?\s*$',
            r'^(nuh\s*uh|uh\s*uh)[\.\!\?]?\s*$',
        ],
        'priority': 5
    },
    'SIMPLE_EXCLAMATION': {
        'patterns': [
            r'^(oh|wow|damn|yippee|teehee|oof|yay|woah|whoa|nice|cool|lol|lmao)[\.\!\?]*\s*$',
            r'^o+h+[\.\!\?]*\s*$',
        ],
        'priority': 5
    },

    # =========================================================================
    # PHASE 2 - EXPANDED COVERAGE PATTERNS
    # =========================================================================
    'SELF_STATEMENT': {
        # User sharing their state/feelings/beliefs
        'patterns': [
            r'\bi\s+(am|was|feel|felt|think|believe|want|need|have|know|guess|suppose)\b',
            r'\bi\'?m\s+(feeling|doing|going|trying|just)\b',
            r'\bmy\s+(mind|heart|soul|brain|head)\b',
        ],
        'priority': 4  # Low priority - catch statements about self
    },
    'BOT_CAPABILITY': {
        # Questions about what the bot can do
        'patterns': [
            r'\b(do|can|could|will|would)\s+you\s+(know|have|remember|recall|tell|show|help)\b',
            r'\bcan\s+you\b',
            r'\bdo\s+you\s+(have|know|like|want|need|feel|think)\b',
        ],
        'priority': 6
    },
    'IMPERATIVE': {
        # Commands and requests
        'patterns': [
            r'^(tell|show|give|let|make|help|explain|describe)\s+me\b',
            r'^(look|watch|see|check|listen)\b',
            r'^(try|do|say|repeat|answer)\b',
        ],
        'priority': 5
    },
    'SHARING': {
        # User sharing content/images/links
        # Note: "this is" only at start to avoid matching mid-sentence
        'patterns': [
            r'^(this\s+is|here\'?s|here\s+is|look\s+at|check\s+out)\b',
            r'\bi\'?m\s+(showing|sharing|sending)\b',
            r'\b(sent|sending)\s+(you|a|an|the)\b',
        ],
        'priority': 5
    },
    'EMOTIONAL_REACTION': {
        # Short emotional responses
        'patterns': [
            r'^[\:\;][\_\-]?[\(\)\[\]DdPpOo3]+\s*$',  # Emoticons :) :( ;) :D :P
            r'^[<>]?[\:\;][\_\-]?[\(\)\[\]DdPpOo3]+\s*$',
            r'^\s*[\U0001F600-\U0001F64F]+\s*$',  # Emoji-only messages
            r'^(hm+|um+|ah+|eh+|oh+|uh+)[\.\!\?]*\s*$',  # Thinking sounds
            r'^(haha+|lmao+|rofl|hehe+|hihi+)[\.\!\?]*\s*$',  # Laughter
            r'^(\:\(+|\;\(+|T[_\-]?T|;[_\-];)\s*$',  # Sad faces
        ],
        'priority': 4
    },
    'ROLEPLAY_INVITATION': {
        # User inviting deeper conversation
        # Priority 6 to beat IMPERATIVE's generic "tell me" pattern
        'patterns': [
            r'\b(want\s+to|wanna|let\'?s|shall\s+we|we\s+could|we\s+can)\b.*\??\s*$',
            r'\bgo\s+(deeper|further|on)\b',
            r'\b(tell|teach|show)\s+me\s+more\b',
            r'\bkeep\s+going\b',
        ],
        'priority': 6
    },
    'CORRECTION': {
        # User correcting/clarifying
        'patterns': [
            r'\b(no|not)\s+(that\'?s|it\'?s|i|what|that)\s+(not|wrong|incorrect)\b',
            r'\bi\s+(meant|mean|said|was\s+saying)\b',
            r'\b(actually|technically|well\s+actually)\b',
            r'\b(let\s+me\s+)?(rephrase|clarify|explain)\b',
        ],
        'priority': 5
    },
    'CONFUSION': {
        # User expressing confusion
        'patterns': [
            r'\b(what|huh|wut|wat)\?+\s*$',
            r'\bi\s+don\'?t\s+(understand|get|follow)\b',
            r'\b(confused|lost|puzzled)\b',
            r'\bwhat\s+do\s+you\s+mean\b',
            r'^(\?\?+|huh\?*)\s*$',
        ],
        'priority': 6
    },
}


def detect_intent(message_text, is_question_flag=False):
    """
    Detect user intent from message text.

    Args:
        message_text (str): Raw message content
        is_question_flag (bool): True if message is detected as question

    Returns:
        str or None: Intent name if matched, None for default behavior

    Priority-based matching: Higher priority intents checked first.
    Falls back to None if no intent matches (uses default question/statement pools).
    """
    try:
        text_lower = message_text.lower().strip()
        # Remove bot mentions for cleaner pattern matching
        text_clean = re.sub(r'<@!?\d+>', '', text_lower).strip()

        # Sort intents by priority (highest first)
        sorted_intents = sorted(INTENTS.items(), key=lambda x: x[1]['priority'], reverse=True)

        for intent_name, config in sorted_intents:
            # Skip if question_only constraint not met
            if config.get('question_only') and not is_question_flag:
                continue

            # Check keywords
            if 'keywords' in config:
                for keyword in config['keywords']:
                    if config.get('anywhere'):
                        # Match keyword anywhere in message
                        if keyword in text_clean:
                            logger.debug(f"Intent '{intent_name}' matched via keyword '{keyword}'")
                            return intent_name
                    else:
                        # Match keyword as whole word
                        if re.search(r'\b' + re.escape(keyword) + r'\b', text_clean):
                            logger.debug(f"Intent '{intent_name}' matched via keyword '{keyword}'")
                            return intent_name

            # Check regex patterns
            if 'patterns' in config:
                for pattern in config['patterns']:
                    if re.search(pattern, text_clean, re.IGNORECASE):
                        logger.debug(f"Intent '{intent_name}' matched via pattern '{pattern}'")
                        return intent_name

        # No intent matched
        logger.debug(f"No intent detected for message: '{message_text[:50]}...'")
        return None

    except Exception as e:
        logger.error(f"Intent detection failed: {type(e).__name__}: {e}")
        return None  # Safe fallback


def get_all_intents():
    """Return list of all defined intent names."""
    return list(INTENTS.keys())


def get_intent_priority(intent_name):
    """Get priority value for an intent."""
    if intent_name in INTENTS:
        return INTENTS[intent_name]['priority']
    return 0
