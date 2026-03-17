"""Tests for bot services."""

import pytest

from bot.services.analyzer import analyze_dream_keywords


def test_analyzer_keywords_returns_questions() -> None:
    """Keyword analyzer returns existential questions for pattern-rich text."""
    text = "I was in a tower with many levels, found a glitch in the wall, ran an AI model."
    result = analyze_dream_keywords(text)
    assert "Existential questions" in result
    assert "glitch" in result.lower() or "level" in result.lower() or "AI" in result


def test_analyzer_keywords_fallback_for_generic_text() -> None:
    """Keyword analyzer returns default questions for text without patterns."""
    text = "I ate breakfast and went to work."
    result = analyze_dream_keywords(text)
    assert "Existential questions" in result
    assert "systemic constraint" in result or "dreamer" in result
