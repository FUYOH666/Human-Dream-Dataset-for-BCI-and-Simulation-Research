# Changelog

## [0.1.1] - 2026-03-17

### Fixed

- Long messages: split transcript and analysis into chunks under Telegram 4096 limit
- ASR timeout 600s, LLM timeout 180s for voice up to ~10 min
- Add `test_split_message_under_telegram_limit`

## [0.1.0] - 2026-03-17

### Added

- Initial release: Human Dream Dataset for BCI and Simulation Research
- `docs/HYPOTHESIS.md`: Research hypothesis on systemic prompt constraints (agent experiment, falsifiability, connection to simulation research)
- `docs/RECORDING_GUIDE.md`: Practical dream capture tips (Place/Events/Participants tags, voice vs. writing, immediacy)
- **Telegram Bot** (`bot/`): Voice → ASR (8001) → transcript → LLM (8005 or OpenRouter) → structured analysis. Keyword fallback when LLM unavailable.
- **Interpretation experiment (open call):** Embedding + Reranker for dream interpretation through indexed books/knowledge bases. See README.
- README with abstract, methodology, key findings
- Full dream catalog (60 episodes, anonymized)
- Patterns summary (recurring motifs table)
- 5 anonymized raw examples
- `dream_analyzer.py`: keyword-based extraction of existential questions from dream text
- MIT License
- GitHub Actions workflow for auto-updating "Last updated" in README
- Public GitHub repository: https://github.com/FUYOH666/Human-Dream-Dataset-for-BCI-and-Simulation-Research
