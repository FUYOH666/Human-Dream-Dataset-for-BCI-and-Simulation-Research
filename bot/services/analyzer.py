"""Keyword-based dream analyzer (fallback when LLM unavailable)."""

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Add project root for analysis import
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from analysis.dream_analyzer import analyze as _analyze


def analyze_dream_keywords(text: str) -> str:
    """
    Extract existential questions from dream text using keyword patterns.

    Used as fallback when LLM is unavailable.
    """
    questions = _analyze(text)
    lines = [
        "**Keyword analysis** (LLM unavailable):",
        "",
        "**Existential questions:**",
    ]
    for i, q in enumerate(questions, 1):
        lines.append(f"  {i}. {q}")
    return "\n".join(lines)
