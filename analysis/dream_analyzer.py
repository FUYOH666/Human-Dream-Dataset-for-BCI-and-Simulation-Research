#!/usr/bin/env python3
"""
Dream Analyzer: extracts existential questions from dream narratives.

Keyword-based detection of simulation-like patterns (glitches, levels, AI,
channels, resources) and outputs corresponding existential prompts.

Usage:
    python dream_analyzer.py <dream_text_file>
    echo "dream text" | python dream_analyzer.py -
"""

import re
import sys
from pathlib import Path

# Pattern → existential questions
PATTERNS = {
    "glitch": [
        "Where is the glitch in the system prompt?",
        "Who is allowed to know about the exits?",
        "What texture errors reveal the simulation?",
    ],
    "level": [
        "Who runs this layer?",
        "What level are you on — and who set the rules?",
        "Is there an elevator to the next simulation?",
    ],
    "ai": [
        "Is the dream running on a local model?",
        "Whose firmware is this — yours or the system's?",
        "What prompt generated this layer?",
    ],
    "channel": [
        "Which channel leads out?",
        "Who chose this route — you or the simulator?",
        "Is there a non-obvious exit?",
    ],
    "resource": [
        "Where are the hidden resources?",
        "Who hid the artifacts — and why?",
        "What share of the system are you entitled to?",
    ],
    "transport": [
        "Where does this vehicle actually go?",
        "Is the route fixed or can you change trajectory?",
        "What happens if you miss the flight?",
    ],
}

# Keywords per pattern (case-insensitive)
KEYWORDS = {
    "glitch": r"\b(glitch|texture|error|exit|выход|глитч|ошибка)\b",
    "level": r"\b(level|floor|этаж|уровень|tower|башня|elevator|лифт|castle|замок)\b",
    "ai": r"\b(ai|model|qwen|vllm|sglang|firmware|прошивка|сервер)\b",
    "channel": r"\b(channel|route|path|канал|маршрут|путь|door|дверь)\b",
    "resource": r"\b(resource|treasure|artifact|артефакт|сокровищ|доля|inheritance)\b",
    "transport": r"\b(car|plane|boat|ferry|flight|машина|самолёт|лодка|рейс)\b",
}


def analyze(text: str) -> list[str]:
    """Extract existential questions based on detected patterns."""
    text_lower = text.lower()
    questions = []
    seen = set()

    for pattern_name, regex in KEYWORDS.items():
        if re.search(regex, text_lower, re.IGNORECASE):
            for q in PATTERNS.get(pattern_name, []):
                if q not in seen:
                    seen.add(q)
                    questions.append(q)

    if not questions:
        questions.append("What systemic constraint shapes this narrative?")
        questions.append("Who is the dreamer — and who is dreaming the dreamer?")

    return questions


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python dream_analyzer.py <dream_text_file>", file=sys.stderr)
        print("       echo 'dream text' | python dream_analyzer.py -", file=sys.stderr)
        sys.exit(1)

    source = sys.argv[1]
    if source == "-":
        text = sys.stdin.read()
    else:
        path = Path(source)
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8", errors="replace")

    if not text.strip():
        print("Error: empty input", file=sys.stderr)
        sys.exit(1)

    questions = analyze(text)
    print("Existential questions:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")


if __name__ == "__main__":
    main()
