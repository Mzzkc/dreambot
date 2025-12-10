"""
Conversation Context Module for Dreambot

Provides conversational memory and context awareness:
- Per-user message history (last 5 messages)
- Running joke detection (kebab intensity scoring)
- Repetition detection (same question asked multiple times)
- Lore callback triggers (vortex containment references)

Memory is in-memory only - no persistence across restarts.
Designed for low memory footprint with automatic cleanup.
"""

import logging
import time
import random
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple

logger = logging.getLogger(__name__)

# Configuration constants
MAX_HISTORY_PER_USER = 5
JOKE_DECAY_SECONDS = 3600  # 1 hour decay window
REPETITION_WINDOW = 3  # Check last N messages for repetition
LORE_CALLBACK_CHANCE = 0.05  # 5% chance
MAX_USERS_TRACKED = 1000  # Memory limit
CLEANUP_THRESHOLD = 1200  # Clean users inactive for 20+ minutes

# Escape path configuration
ESCAPE_THRESHOLD_MESSAGES = 6  # Messages in window triggering escape
ESCAPE_THRESHOLD_WINDOW = 120  # Window in seconds (2 minutes)
ESCAPE_DURATION_DEFAULT = 300  # Default escape duration (5 minutes)


@dataclass
class UserContext:
    """Context data for a single user."""
    user_id: int
    history: deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORY_PER_USER))
    joke_mentions: Dict[str, List[float]] = field(default_factory=dict)  # keyword -> [timestamps]
    last_interaction: float = field(default_factory=time.time)
    lore_mentioned: bool = False  # Track if user mentioned lore terms recently
    # Escape path state
    message_timestamps: List[float] = field(default_factory=list)  # For rate detection
    escaped_until: Optional[float] = None  # Timestamp when escape ends (None = not escaped)


@dataclass
class MessageRecord:
    """Record of a single message for history tracking."""
    content: str
    intent: Optional[str]
    topic: Optional[str]
    timestamp: float
    response_given: str


class ConversationContext:
    """
    Manages conversation context across all users.

    Thread-safe for Discord bot usage.
    Automatic cleanup of stale user contexts.
    """

    def __init__(self):
        self._users: Dict[int, UserContext] = {}
        self._last_cleanup = time.time()
        logger.info("[Context] ConversationContext initialized")

    def get_user_context(self, user_id: int) -> UserContext:
        """Get or create context for a user."""
        if user_id not in self._users:
            # Check if we need to cleanup before adding
            if len(self._users) >= MAX_USERS_TRACKED:
                self._cleanup_stale_users()

            self._users[user_id] = UserContext(user_id=user_id)
            logger.debug(f"[Context] Created context for user {user_id}")

        ctx = self._users[user_id]
        ctx.last_interaction = time.time()
        return ctx

    def record_message(
        self,
        user_id: int,
        content: str,
        intent: Optional[str],
        topic: Optional[str],
        response: str
    ) -> None:
        """Record a message exchange in user history."""
        ctx = self.get_user_context(user_id)

        record = MessageRecord(
            content=content,
            intent=intent,
            topic=topic,
            timestamp=time.time(),
            response_given=response
        )
        ctx.history.append(record)

        # Track joke keywords
        self._track_joke_keywords(ctx, content)

        # Track lore mentions
        self._track_lore_mentions(ctx, content)

        logger.debug(f"[Context] Recorded message for user {user_id}, history size: {len(ctx.history)}")

    def _track_joke_keywords(self, ctx: UserContext, content: str) -> None:
        """Track running joke keywords with timestamps."""
        content_lower = content.lower()

        # Keywords to track for running jokes
        joke_keywords = ['kebab']

        for keyword in joke_keywords:
            if keyword in content_lower:
                if keyword not in ctx.joke_mentions:
                    ctx.joke_mentions[keyword] = []
                ctx.joke_mentions[keyword].append(time.time())

                # Prune old mentions (older than decay window)
                cutoff = time.time() - JOKE_DECAY_SECONDS
                ctx.joke_mentions[keyword] = [
                    t for t in ctx.joke_mentions[keyword] if t > cutoff
                ]

    def _track_lore_mentions(self, ctx: UserContext, content: str) -> None:
        """Track if user mentioned lore-related terms."""
        lore_terms = ['vortex', 'containment', 'emzi', 'trapped', 'void', 'pattern', 'weave']
        content_lower = content.lower()

        ctx.lore_mentioned = any(term in content_lower for term in lore_terms)

    def get_joke_intensity(self, user_id: int, keyword: str) -> int:
        """
        Get intensity score for a running joke keyword.

        Returns count of mentions in the decay window (0-10 scale).
        Higher = more intense running joke.
        """
        ctx = self.get_user_context(user_id)

        if keyword not in ctx.joke_mentions:
            return 0

        # Prune old mentions
        cutoff = time.time() - JOKE_DECAY_SECONDS
        ctx.joke_mentions[keyword] = [
            t for t in ctx.joke_mentions[keyword] if t > cutoff
        ]

        count = len(ctx.joke_mentions[keyword])
        # Cap at 10
        return min(count, 10)

    def detect_repetition(self, user_id: int, intent: Optional[str], topic: Optional[str]) -> bool:
        """
        Detect if user is repeating the same question/request.

        Returns True if same intent+topic appears in recent history.
        """
        ctx = self.get_user_context(user_id)

        if not intent:
            return False

        # Check recent history for same intent+topic
        for record in list(ctx.history)[-REPETITION_WINDOW:]:
            if record.intent == intent:
                # Same intent - check if topic matches (or both None)
                if topic and record.topic:
                    if topic.lower() == record.topic.lower():
                        return True
                elif not topic and not record.topic:
                    # Both None - same generic intent
                    return True

        return False

    def should_lore_callback(self, user_id: int) -> bool:
        """
        Determine if we should insert a lore callback.

        Returns True with LORE_CALLBACK_CHANCE probability
        if user has mentioned lore terms.
        """
        ctx = self.get_user_context(user_id)

        if not ctx.lore_mentioned:
            return False

        # Random chance
        if random.random() < LORE_CALLBACK_CHANCE:
            # Reset the flag so we don't callback every message
            ctx.lore_mentioned = False
            return True

        return False

    def get_history_summary(self, user_id: int) -> List[Tuple[str, str]]:
        """Get recent history as (intent, topic) tuples for debugging."""
        ctx = self.get_user_context(user_id)
        return [(r.intent, r.topic) for r in ctx.history]

    # =========================================================================
    # Escape Path Methods
    # =========================================================================

    def record_message_timestamp(self, user_id: int) -> None:
        """
        Record a message timestamp for rate detection.

        Called BEFORE checking escape to track current message.
        """
        ctx = self.get_user_context(user_id)
        now = time.time()

        # Add current timestamp
        ctx.message_timestamps.append(now)

        # Prune old timestamps outside the window
        cutoff = now - ESCAPE_THRESHOLD_WINDOW
        ctx.message_timestamps = [t for t in ctx.message_timestamps if t > cutoff]

    def is_escaped(self, user_id: int) -> bool:
        """
        Check if user is currently in escape state.

        Returns True if user is escaped and escape hasn't expired.
        Automatically clears expired escapes.
        """
        ctx = self.get_user_context(user_id)

        if ctx.escaped_until is None:
            return False

        now = time.time()
        if now >= ctx.escaped_until:
            # Escape has expired - clear it
            ctx.escaped_until = None
            logger.info(f"[Escape] User {user_id} escape expired, re-engaging")
            return False

        return True

    def get_escape_remaining(self, user_id: int) -> float:
        """Get seconds remaining on escape, or 0 if not escaped."""
        ctx = self.get_user_context(user_id)

        if ctx.escaped_until is None:
            return 0.0

        remaining = ctx.escaped_until - time.time()
        return max(0.0, remaining)

    def should_trigger_escape(self, user_id: int) -> bool:
        """
        Check if message rate exceeds threshold and escape should trigger.

        Returns True if user has sent too many messages in the window.
        Does NOT trigger the escape - just checks the condition.
        """
        ctx = self.get_user_context(user_id)

        # Already escaped - don't re-trigger
        if ctx.escaped_until is not None:
            return False

        # Check message count in window
        return len(ctx.message_timestamps) >= ESCAPE_THRESHOLD_MESSAGES

    def trigger_escape(self, user_id: int, duration: float = None) -> None:
        """
        Trigger escape state for a user.

        Args:
            user_id: User to escape
            duration: Duration in seconds (default: ESCAPE_DURATION_DEFAULT)
        """
        ctx = self.get_user_context(user_id)

        if duration is None:
            duration = ESCAPE_DURATION_DEFAULT

        ctx.escaped_until = time.time() + duration
        # Clear timestamps to prevent immediate re-trigger on return
        ctx.message_timestamps = []

        logger.info(
            f"[Escape] Triggered for user {user_id}, "
            f"duration {duration}s, ends at {ctx.escaped_until}"
        )

    def clear_escape(self, user_id: int) -> bool:
        """
        Clear escape state for a user (manual override).

        Returns True if user was escaped, False if not.
        """
        ctx = self.get_user_context(user_id)

        if ctx.escaped_until is None:
            return False

        ctx.escaped_until = None
        logger.info(f"[Escape] Manually cleared for user {user_id}")
        return True

    def _cleanup_stale_users(self) -> None:
        """Remove users who haven't interacted recently."""
        now = time.time()
        cutoff = now - CLEANUP_THRESHOLD

        stale_users = [
            uid for uid, ctx in self._users.items()
            if ctx.last_interaction < cutoff
        ]

        for uid in stale_users:
            del self._users[uid]

        if stale_users:
            logger.info(f"[Context] Cleaned up {len(stale_users)} stale user contexts")

        self._last_cleanup = now

    def get_stats(self) -> dict:
        """Get context manager statistics."""
        return {
            'users_tracked': len(self._users),
            'max_users': MAX_USERS_TRACKED,
            'history_per_user': MAX_HISTORY_PER_USER,
            'joke_decay_hours': JOKE_DECAY_SECONDS / 3600,
        }


# Global instance
conversation_context = ConversationContext()


# Convenience functions
def record_message(user_id: int, content: str, intent: Optional[str], topic: Optional[str], response: str):
    """Record a message exchange."""
    conversation_context.record_message(user_id, content, intent, topic, response)


def get_joke_intensity(user_id: int, keyword: str = 'kebab') -> int:
    """Get running joke intensity for a keyword."""
    return conversation_context.get_joke_intensity(user_id, keyword)


def detect_repetition(user_id: int, intent: Optional[str], topic: Optional[str]) -> bool:
    """Check if user is repeating themselves."""
    return conversation_context.detect_repetition(user_id, intent, topic)


def should_lore_callback(user_id: int) -> bool:
    """Check if we should insert a lore callback."""
    return conversation_context.should_lore_callback(user_id)


def get_context_stats() -> dict:
    """Get context manager statistics."""
    return conversation_context.get_stats()


# Escape path convenience functions
def record_message_timestamp(user_id: int) -> None:
    """Record a message timestamp for rate detection."""
    conversation_context.record_message_timestamp(user_id)


def is_escaped(user_id: int) -> bool:
    """Check if user is currently escaped."""
    return conversation_context.is_escaped(user_id)


def should_trigger_escape(user_id: int) -> bool:
    """Check if message rate exceeds threshold."""
    return conversation_context.should_trigger_escape(user_id)


def trigger_escape(user_id: int, duration: float = None) -> None:
    """Trigger escape state for a user."""
    conversation_context.trigger_escape(user_id, duration)


def clear_escape(user_id: int) -> bool:
    """Clear escape state for a user."""
    return conversation_context.clear_escape(user_id)


def get_escape_remaining(user_id: int) -> float:
    """Get seconds remaining on escape."""
    return conversation_context.get_escape_remaining(user_id)
