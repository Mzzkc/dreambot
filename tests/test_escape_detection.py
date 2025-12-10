"""
Unit tests for escape path detection.
"""

import pytest
import sys
import time
from unittest.mock import patch

sys.path.insert(0, 'src')

from events.conversation_context import (
    ConversationContext,
    ESCAPE_THRESHOLD_MESSAGES,
    ESCAPE_THRESHOLD_WINDOW,
    ESCAPE_DURATION_DEFAULT,
)


class TestEscapeDetection:
    """Test escape path rate detection."""

    def setup_method(self):
        """Create fresh context for each test."""
        self.ctx = ConversationContext()

    def test_no_escape_initial_state(self):
        """User should not be escaped initially."""
        assert not self.ctx.is_escaped(12345)

    def test_no_escape_after_single_message(self):
        """Single message should not trigger escape."""
        self.ctx.record_message_timestamp(12345)
        assert not self.ctx.should_trigger_escape(12345)

    def test_no_escape_below_threshold(self):
        """Messages below threshold should not trigger escape."""
        user_id = 12345
        # Send threshold - 1 messages
        for _ in range(ESCAPE_THRESHOLD_MESSAGES - 1):
            self.ctx.record_message_timestamp(user_id)

        assert not self.ctx.should_trigger_escape(user_id)

    def test_escape_triggers_at_threshold(self):
        """Should trigger escape when threshold is reached."""
        user_id = 12345
        # Send exactly threshold messages
        for _ in range(ESCAPE_THRESHOLD_MESSAGES):
            self.ctx.record_message_timestamp(user_id)

        assert self.ctx.should_trigger_escape(user_id)

    def test_escape_triggers_above_threshold(self):
        """Should trigger escape when above threshold."""
        user_id = 12345
        # Send more than threshold
        for _ in range(ESCAPE_THRESHOLD_MESSAGES + 5):
            self.ctx.record_message_timestamp(user_id)

        assert self.ctx.should_trigger_escape(user_id)

    def test_is_escaped_after_trigger(self):
        """User should be escaped after trigger_escape is called."""
        user_id = 12345
        self.ctx.trigger_escape(user_id)
        assert self.ctx.is_escaped(user_id)

    def test_escape_remaining_time(self):
        """Escape remaining should return positive value when escaped."""
        user_id = 12345
        self.ctx.trigger_escape(user_id, duration=60)

        remaining = self.ctx.get_escape_remaining(user_id)
        assert 58 < remaining <= 60  # Allow small timing variance

    def test_escape_remaining_zero_when_not_escaped(self):
        """Escape remaining should be 0 when not escaped."""
        assert self.ctx.get_escape_remaining(12345) == 0.0

    def test_no_retrigger_while_escaped(self):
        """Should not trigger escape while already escaped."""
        user_id = 12345
        self.ctx.trigger_escape(user_id)

        # Try to trigger again
        for _ in range(ESCAPE_THRESHOLD_MESSAGES + 5):
            self.ctx.record_message_timestamp(user_id)

        # should_trigger_escape returns False because already escaped
        assert not self.ctx.should_trigger_escape(user_id)

    def test_clear_escape(self):
        """Manual clear should remove escape state."""
        user_id = 12345
        self.ctx.trigger_escape(user_id)
        assert self.ctx.is_escaped(user_id)

        result = self.ctx.clear_escape(user_id)
        assert result is True
        assert not self.ctx.is_escaped(user_id)

    def test_clear_escape_returns_false_when_not_escaped(self):
        """Clear should return False when user wasn't escaped."""
        result = self.ctx.clear_escape(12345)
        assert result is False


class TestEscapeExpiration:
    """Test escape expiration logic."""

    def setup_method(self):
        """Create fresh context for each test."""
        self.ctx = ConversationContext()

    def test_escape_expires_after_duration(self):
        """Escape should auto-expire after duration."""
        user_id = 12345

        # Mock time to test expiration
        with patch('events.conversation_context.time.time') as mock_time:
            # Start at time 1000
            mock_time.return_value = 1000
            self.ctx.trigger_escape(user_id, duration=60)

            # Still escaped at time 1030
            mock_time.return_value = 1030
            assert self.ctx.is_escaped(user_id)

            # Escaped at time 1059
            mock_time.return_value = 1059
            assert self.ctx.is_escaped(user_id)

            # Not escaped at time 1060 (exactly at expiration)
            mock_time.return_value = 1060
            assert not self.ctx.is_escaped(user_id)

    def test_escape_expires_clears_state(self):
        """Expiration should clear escaped_until field."""
        user_id = 12345

        with patch('events.conversation_context.time.time') as mock_time:
            mock_time.return_value = 1000
            self.ctx.trigger_escape(user_id, duration=10)

            # After expiration, check clears state
            mock_time.return_value = 1011
            self.ctx.is_escaped(user_id)  # This should clear the state

            # Now get_user_context should show None
            ctx = self.ctx.get_user_context(user_id)
            assert ctx.escaped_until is None


class TestEscapeTimestampPruning:
    """Test that old timestamps are pruned correctly."""

    def setup_method(self):
        """Create fresh context for each test."""
        self.ctx = ConversationContext()

    def test_timestamps_pruned_outside_window(self):
        """Old timestamps should be pruned outside window."""
        user_id = 12345

        with patch('events.conversation_context.time.time') as mock_time:
            # Record messages at time 1000
            mock_time.return_value = 1000
            for _ in range(3):
                self.ctx.record_message_timestamp(user_id)

            # Record more messages after window has passed
            mock_time.return_value = 1000 + ESCAPE_THRESHOLD_WINDOW + 10
            for _ in range(2):
                self.ctx.record_message_timestamp(user_id)

            # Should only have 2 timestamps (old ones pruned)
            ctx = self.ctx.get_user_context(user_id)
            assert len(ctx.message_timestamps) == 2

    def test_no_escape_if_messages_spread_across_windows(self):
        """Messages spread across windows shouldn't trigger escape."""
        user_id = 12345

        with patch('events.conversation_context.time.time') as mock_time:
            # Record threshold-1 messages at time 1000
            mock_time.return_value = 1000
            for _ in range(ESCAPE_THRESHOLD_MESSAGES - 1):
                self.ctx.record_message_timestamp(user_id)

            # Record 2 more messages after window expires
            mock_time.return_value = 1000 + ESCAPE_THRESHOLD_WINDOW + 10
            self.ctx.record_message_timestamp(user_id)
            self.ctx.record_message_timestamp(user_id)

            # Should NOT trigger (old messages pruned)
            assert not self.ctx.should_trigger_escape(user_id)


class TestEscapeDefaults:
    """Test escape configuration defaults."""

    def test_threshold_messages_is_reasonable(self):
        """Threshold should be reasonable (5-10 messages)."""
        assert 4 <= ESCAPE_THRESHOLD_MESSAGES <= 12

    def test_threshold_window_is_reasonable(self):
        """Window should be reasonable (1-5 minutes)."""
        assert 60 <= ESCAPE_THRESHOLD_WINDOW <= 300

    def test_default_duration_is_reasonable(self):
        """Default escape duration should be reasonable (2-15 minutes)."""
        assert 120 <= ESCAPE_DURATION_DEFAULT <= 900


class TestMultipleUsers:
    """Test escape behavior with multiple users."""

    def setup_method(self):
        """Create fresh context for each test."""
        self.ctx = ConversationContext()

    def test_escape_independent_per_user(self):
        """Escape state should be independent per user."""
        user_a = 11111
        user_b = 22222

        # Escape user A
        self.ctx.trigger_escape(user_a)

        # User B should not be affected
        assert self.ctx.is_escaped(user_a)
        assert not self.ctx.is_escaped(user_b)

    def test_rate_tracking_independent_per_user(self):
        """Rate tracking should be independent per user."""
        user_a = 11111
        user_b = 22222

        # User A sends threshold messages
        for _ in range(ESCAPE_THRESHOLD_MESSAGES):
            self.ctx.record_message_timestamp(user_a)

        # User B sends 1 message
        self.ctx.record_message_timestamp(user_b)

        # Only user A should trigger
        assert self.ctx.should_trigger_escape(user_a)
        assert not self.ctx.should_trigger_escape(user_b)
