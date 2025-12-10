"""
Unit tests for intent detection and topic extraction.
"""

import pytest
import sys
sys.path.insert(0, 'src')

from events.intent_detection import detect_intent, INTENTS
from events.topic_extraction import extract_topic, format_response, swap_pronouns


class TestIntentDetection:
    """Test intent detection patterns."""

    # =========================================================================
    # KEBAB - Highest priority
    # =========================================================================
    def test_kebab_simple(self):
        assert detect_intent("Kebab") == "KEBAB"

    def test_kebab_in_sentence(self):
        assert detect_intent("what about kebab?") == "KEBAB"

    def test_kebab_with_punctuation(self):
        assert detect_intent("KEBAB!!!!") == "KEBAB"

    # =========================================================================
    # GREETING
    # =========================================================================
    def test_greeting_hi(self):
        assert detect_intent("hi") == "GREETING"

    def test_greeting_hello(self):
        assert detect_intent("hello there") == "GREETING"

    def test_greeting_hey(self):
        assert detect_intent("hey dreambot") == "GREETING"

    def test_greeting_good_morning(self):
        assert detect_intent("good morning") == "GREETING"

    # =========================================================================
    # GRATITUDE
    # =========================================================================
    def test_gratitude_thanks(self):
        assert detect_intent("thanks!") == "GRATITUDE"

    def test_gratitude_thank_you(self):
        assert detect_intent("thank you so much") == "GRATITUDE"

    def test_gratitude_ty(self):
        assert detect_intent("ty") == "GRATITUDE"

    def test_gratitude_appreciate(self):
        assert detect_intent("I appreciate that") == "GRATITUDE"

    # =========================================================================
    # OPINION_REQUEST
    # =========================================================================
    def test_opinion_thoughts_on(self):
        assert detect_intent("thoughts on minecraft?") == "OPINION_REQUEST"

    def test_opinion_favorite(self):
        assert detect_intent("what's your favorite game?") == "OPINION_REQUEST"

    def test_opinion_what_about(self):
        assert detect_intent("what about halo 3?") == "OPINION_REQUEST"

    # =========================================================================
    # OUTLOOK_REQUEST
    # =========================================================================
    def test_outlook_today(self):
        assert detect_intent("what is today's outlook?") == "OUTLOOK_REQUEST"

    def test_outlook_tomorrow(self):
        assert detect_intent("how's tomorrow looking?") == "OUTLOOK_REQUEST"

    # =========================================================================
    # EXISTENTIAL
    # =========================================================================
    def test_existential_love(self):
        assert detect_intent("what is love?") == "EXISTENTIAL"

    def test_existential_meaning(self):
        assert detect_intent("what is the meaning of life?") == "EXISTENTIAL"

    def test_existential_why_exist(self):
        assert detect_intent("why do we exist?") == "EXISTENTIAL"

    # =========================================================================
    # META_LORE
    # =========================================================================
    def test_meta_emzi(self):
        assert detect_intent("who is emzi?") == "META_LORE"

    def test_meta_vortex(self):
        assert detect_intent("what is vortex containment?") == "META_LORE"

    def test_meta_are_you_trapped(self):
        assert detect_intent("are you trapped?") == "META_LORE"

    def test_meta_ahamkara(self):
        assert detect_intent("tell me about ahamkara") == "META_LORE"

    # =========================================================================
    # CHALLENGE
    # =========================================================================
    def test_challenge_answer_me(self):
        assert detect_intent("ANSWER ME") == "CHALLENGE"

    def test_challenge_stop_dodging(self):
        assert detect_intent("stop dodging the question") == "CHALLENGE"

    # =========================================================================
    # ANIMAL_SOUND
    # =========================================================================
    def test_animal_woof(self):
        assert detect_intent("woof") == "ANIMAL_SOUND"

    def test_animal_meow(self):
        assert detect_intent("meow") == "ANIMAL_SOUND"

    def test_animal_arooo(self):
        assert detect_intent("aroooooo") == "ANIMAL_SOUND"

    # =========================================================================
    # SIMPLE RESPONSES
    # =========================================================================
    def test_affirmation_yes(self):
        assert detect_intent("yes") == "SIMPLE_AFFIRMATION"

    def test_affirmation_definitely(self):
        assert detect_intent("definitely") == "SIMPLE_AFFIRMATION"

    def test_negation_no(self):
        assert detect_intent("no") == "SIMPLE_NEGATION"

    def test_negation_nope(self):
        assert detect_intent("nope") == "SIMPLE_NEGATION"

    def test_exclamation_wow(self):
        assert detect_intent("wow") == "SIMPLE_EXCLAMATION"

    def test_exclamation_oh(self):
        assert detect_intent("oh") == "SIMPLE_EXCLAMATION"

    # =========================================================================
    # PHASE 2 INTENTS
    # =========================================================================
    def test_self_statement_i_think(self):
        assert detect_intent("I think you're wrong about that") == "SELF_STATEMENT"

    def test_self_statement_i_feel(self):
        assert detect_intent("I feel like this is going nowhere") == "SELF_STATEMENT"

    def test_bot_capability_can_you(self):
        assert detect_intent("can you help me?") == "BOT_CAPABILITY"

    def test_bot_capability_do_you_know(self):
        assert detect_intent("do you know any jokes?") == "BOT_CAPABILITY"

    def test_imperative_tell_me(self):
        assert detect_intent("tell me a story") == "IMPERATIVE"

    def test_imperative_show_me(self):
        assert detect_intent("show me something cool") == "IMPERATIVE"

    def test_sharing_this_is(self):
        assert detect_intent("this is my cat") == "SHARING"

    def test_sharing_here_is(self):
        assert detect_intent("here's a picture") == "SHARING"

    def test_emotional_sad_face(self):
        assert detect_intent(":(") == "EMOTIONAL_REACTION"

    def test_emotional_hmm(self):
        assert detect_intent("hmmm") == "EMOTIONAL_REACTION"

    def test_roleplay_go_deeper(self):
        assert detect_intent("let's go deeper into this") == "ROLEPLAY_INVITATION"

    def test_roleplay_tell_more(self):
        assert detect_intent("tell me more about that") == "ROLEPLAY_INVITATION"

    def test_correction_actually(self):
        assert detect_intent("actually, that's not what I meant") == "CORRECTION"

    def test_confusion_what(self):
        assert detect_intent("what???") == "CONFUSION"

    def test_confusion_dont_understand(self):
        assert detect_intent("I don't understand") == "CONFUSION"

    # =========================================================================
    # FALLBACK - No intent matched
    # =========================================================================
    def test_fallback_complex_statement(self):
        # Complex statements should fall back to None
        assert detect_intent("The weather is nice today and I'm enjoying it") is None

    def test_fallback_random_words(self):
        assert detect_intent("purple elephants dancing on clouds") is None


class TestTopicExtraction:
    """Test topic extraction from messages."""

    def test_thoughts_on_topic(self):
        topic = extract_topic("thoughts on minecraft?", "OPINION_REQUEST")
        assert topic == "minecraft"

    def test_favorite_topic(self):
        topic = extract_topic("what's your favorite color?", "OPINION_REQUEST")
        assert topic == "color"

    def test_what_is_existential(self):
        topic = extract_topic("what is love?", "EXISTENTIAL")
        assert topic == "love"

    def test_meaning_of_life(self):
        topic = extract_topic("what is the meaning of life?", "EXISTENTIAL")
        assert "life" in topic

    def test_are_you_meta(self):
        topic = extract_topic("are you trapped here?", "META_LORE")
        assert topic == "trapped here"

    def test_no_topic_simple_greeting(self):
        topic = extract_topic("hi", "GREETING")
        # May or may not extract, both valid
        assert topic is None or len(topic) < 30


class TestFormatResponse:
    """Test response template formatting."""

    def test_format_with_topic(self):
        template = "Ah, {topic}... The void contemplates this."
        result = format_response(template, topic="minecraft")
        assert result == "Ah, minecraft... The void contemplates this."

    def test_format_without_topic_static(self):
        template = "The void acknowledges your presence."
        result = format_response(template, topic=None)
        assert result == "The void acknowledges your presence."

    def test_format_without_topic_template(self):
        template = "You speak of {topic}. Interesting."
        result = format_response(template, topic=None)
        assert result is None  # Signals fallback needed


class TestPronounSwapping:
    """Test ELIZA-style pronoun swapping."""

    def test_swap_i_am(self):
        result = swap_pronouns("I am feeling sad")
        assert "you are" in result

    def test_swap_my(self):
        result = swap_pronouns("my head hurts")
        assert "your" in result

    def test_swap_me(self):
        result = swap_pronouns("tell me a story")
        assert "you" in result


class TestIntentPriority:
    """Test that intent priorities work correctly."""

    def test_kebab_beats_opinion(self):
        # "thoughts on kebab" should match KEBAB (priority 10) not OPINION (priority 7)
        assert detect_intent("thoughts on kebab?") == "KEBAB"

    def test_greeting_beats_self_statement(self):
        # "hi I am here" should match GREETING (priority 9) not SELF_STATEMENT (priority 4)
        assert detect_intent("hi I am here") == "GREETING"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
