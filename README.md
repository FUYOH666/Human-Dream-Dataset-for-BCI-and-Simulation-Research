# Human Dream Dataset: Metabolic Modulation of Consciousness & Simulation-Like Patterns

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/FUYOH666/Human-Dream-Dataset-for-BCI-and-Simulation-Research)

**Self-experiment by independent researcher (34 y.o., 9 months of daily dream recall training)**

80–90 dream episodes, metabolic modulation (keto, fasting), simulation-like patterns. Open dataset + Telegram bot for recording and analysis.

---

## Abstract

Collected 80–90 dream episodes across ~50 reports. Strict keto + calorie deficit + periodic 48h autophagy triggered extreme cognitive clarity and explosion of vivid, non-terrestrial dreams. Identified recurring simulation-like patterns (texture glitches, multi-level systems, hidden resources, choice of "channels").

Dataset is openly shared for BCI, simulation research, and anyone studying consciousness expansion.

**Note:** AI tools suggested this could be useful for research companies working on consciousness, BCI, or internal-state decoding. If it happens to be relevant for your work — please study, ask questions. Happy to share observations and collaborate.

## Methodology

- **Baseline:** Never recorded dreams before.
- **Intervention:** 4 weeks strict keto + 2 meals/day + 48h fasting every 3–4 weeks + daily sport.
- **Controlled tests:** Sugar, alcohol, magnesium citrate before bed, carbohydrate intake in the evening.
- **Supporting tools:** Wearable (e.g. Whoop) for tracking physical load and recovery — helps calibrate exercise volume for the "physical interface."
- **Recording:** Immediate upon waking (voice notes → text). See [docs/RECORDING_GUIDE.md](docs/RECORDING_GUIDE.md) for practical tips: quick tags (Place, Events, Participants), voice vs. writing, and why detail matters.

## Key Findings

### Physiological Triggers

- **Deep keto** → strongest cognitive clarity and deepest business insights; clarity difficult to compare to everyday baseline.
- Keto + fasting → +300% cognitive clarity + jump from 0–1 to 3–4 dreams/night.
- **Connection:** Keto-induced clarity carries into waking cognition and dream recall — nutrition and sleep are foundational factors for this experiment.
- Trade-offs: low energy for sport, acetone smell (short-term only).
- Sugar/alcohol/magnesium/carbs (evening) — measurable changes in recall and plot depth.

### Dietary factors (subjective observations)

- **Fat quality:** Perceived difference in energy state of the "physical interface" — higher-quality fats vs. processed.
- **Live food:** Home-cooked, minimally processed food (vs. store-bought semi-finished) — subjectively better general state and sleep quality.

*These are observational; open to ideas for objective metrics or replication protocols.*

### Recurring Patterns (simulation-like)

- Texture glitches / exits from system
- Multi-level structures (towers, castles, elevators)
- Hidden resources & inheritance
- Transport / channel choice
- AI integration in dreams (Qwen, vLLM, proshiwki)
- Teamwork & mutual aid without panic

Full catalog: [dataset/dream_catalog.md](dataset/dream_catalog.md)

## Research Hypothesis

A self-evolving agent, when given creator context, asks technical questions and adapts to available data. When creator context is removed, it shifts to existential questions. This suggests a natural constraint — analogous to a "system prompt" — that may limit conscious systems from directly investigating their own origins.

The dream dataset, with its recurring glitches, levels, and channel choices, provides human ground truth for what such constraint phenomenology looks like. The hypothesis is falsifiable: if AI or hybrid systems can bypass these constraints and engage with first-principles questions, that would support the model.

Full elaboration: [docs/HYPOTHESIS.md](docs/HYPOTHESIS.md)

## Implications for Research

- Evidence for "system prompt" constraints on consciousness.
- Ready human ground-truth for training BCI dream-recording algorithms.
- Metabolic pathway to enhance cognition and access altered states (without implant yet).

## How to Use This Dataset

- **BCI / consciousness researchers:** May be useful for sleep-state decoding, cognition enhancement, or internal-state calibration. Open to collaboration.
- **Analysis script:** Run `python analysis/dream_analyzer.py <dream_text_file>` to extract existential questions from dream narratives.
- **Telegram Bot:** Record and analyze dreams via voice or text. See [Bot](#bot) below.

## Bot

A Telegram bot for practical dream recording and analysis: voice → ASR (8001) → transcript → LLM (8005 or OpenRouter) → structured analysis (Place, Events, Participants, patterns, existential questions).

### Setup

```bash
cp .env.example .env
# Edit .env: TELEGRAM_BOT_TOKEN, LOCAL_AI_ASR_BASE_URL, LOCAL_AI_LLM_BASE_URL

uv sync
uv run python -m bot.main
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from @BotFather |
| `LOCAL_AI_ASR_BASE_URL` | Yes | ASR service URL (e.g. http://host:8001) |
| `LOCAL_AI_LLM_BASE_URL` | Yes | LLM service URL (e.g. http://host:8005) |
| `OPENROUTER_API_KEY` | No | For cloud LLM when `USE_OPENROUTER=true` |
| `USE_OPENROUTER` | No | Set to `true` to use OpenRouter instead of local LLM |
| `QDRANT_URL` | No | Qdrant vector store (6333, Docker) for interpretation experiment |
| `LOCAL_AI_EMBEDDING_BASE_URL` | No | Embedding service (9001) for interpretation experiment |
| `LOCAL_AI_RERANKER_BASE_URL` | No | Reranker service (9002) for interpretation experiment |

### Fallback

When LLM is unavailable, the bot uses keyword-based analysis (same logic as `dream_analyzer.py`).

### Services (ports)

All services run locally — dataset collection and analysis are self-hosted.

| Port | Service | Role |
|------|---------|------|
| 6333 | Qdrant (Docker) | Vector store for interpretation experiment |
| 8001 | ASR (Whisper) | Voice → transcript |
| 8005 | LLM (Qwen3.5-27b) | Dream analysis |
| 9001 | Embedding (BGE-M3) | Optional: interpretation experiment |
| 9002 | Reranker (BGE-Reranker-v2-m3) | Optional: interpretation experiment |

## Interpretation Experiment (Open Call)

The full dream dataset is not published here for privacy. But we invite contributions for **interpretation experiments**:

**Idea:** Index one or more books (or knowledge bases) in Qdrant (Docker, port 6333). For a given dream:

1. **Embed** the dream text and book chunks (Embedding service, BGE-M3).
2. **Store & retrieve** in Qdrant via similarity search.
3. **Rerank** results (Reranker service, BGE-Reranker-v2-m3).
4. **Interpret** the dream through the lens of the retrieved knowledge — LLM generates an analysis grounded in that text.

If you have interesting ideas, books, or frameworks that could yield novel interpretations of dream content, we can integrate them. The goal: explore how different knowledge bases (e.g. Jung, neuroscience, simulation hypothesis) reframe the same recorded dreams.

Contact: [GitHub @iamfuyoh](https://github.com/iamfuyoh)

## Repository Structure

```
├── bot/                      # Telegram bot
│   ├── main.py               # Entry point
│   ├── config.py             # Pydantic settings
│   ├── handlers.py           # /start, voice, text
│   ├── prompts/
│   │   └── dream_analysis.txt
│   └── services/
│       ├── asr.py            # ASR client (8001)
│       ├── llm.py            # LLM client (8005 / OpenRouter)
│       └── analyzer.py       # Keyword fallback
├── dataset/
│   ├── dream_catalog.md      # Full catalog (50+ reports)
│   ├── patterns_summary.md   # Recurring motifs table
│   └── raw_examples/         # Anonymized dream samples
├── docs/
│   ├── HYPOTHESIS.md         # Research hypothesis & theoretical framework
│   └── RECORDING_GUIDE.md   # Practical dream capture tips
├── analysis/
│   └── dream_analyzer.py    # Text → existential questions
├── tests/
│   └── test_bot_services.py
```

## Contact

Open for collaboration. [GitHub @iamfuyoh](https://github.com/iamfuyoh)

For research applications: see [STATEMENT.md](STATEMENT.md).

Let's expand awareness beyond biological limits.

---

Last updated: 2026-03-17
License: MIT
