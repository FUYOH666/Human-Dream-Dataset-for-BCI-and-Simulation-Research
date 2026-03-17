"""Telegram bot handlers for dream recording and analysis."""

import logging
from pathlib import Path

from telegram import Update
from telegram.constants import ChatAction, MessageLimit
from telegram.ext import ContextTypes, MessageHandler, CommandHandler

from bot.config import get_settings

# Telegram message limit (4096); use 4000 to stay safe
MAX_MESSAGE_LENGTH = min(4000, MessageLimit.MAX_TEXT_LENGTH - 96)
from bot.services.asr import transcribe as asr_transcribe
from bot.services.llm import analyze_dream as llm_analyze
from bot.services.analyzer import analyze_dream_keywords

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent / "prompts" / "dream_analysis.txt"

START_TEXT = """🌙 *Dream Recording & Analysis*

Record your dream right after waking — voice or text.

*How it works:*
• 🎤 _Voice_ — send a voice message → transcript → analysis
• 📝 _Text_ — write the dream → analysis

*You get:*
Place · Events · Participants · patterns · existential questions

/help — repeat this message"""


def _load_system_prompt() -> str:
    """Load dream analysis system prompt."""
    return PROMPT_PATH.read_text(encoding="utf-8")


def _split_message(text: str, max_len: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split text into chunks under max_len, breaking at newlines when possible."""
    if len(text) <= max_len:
        return [text] if text else []
    chunks: list[str] = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        chunk = text[:max_len]
        last_newline = chunk.rfind("\n")
        if last_newline > max_len // 2:
            chunk = chunk[: last_newline + 1]
            text = text[last_newline + 1 :]
        else:
            text = text[max_len:]
        chunks.append(chunk)
    return chunks


async def _send_chunks(update: Update, text: str) -> None:
    """Send text in chunks under Telegram limit. No parse_mode (LLM output is unpredictable)."""
    for chunk in _split_message(text):
        # Safety: Telegram limit 4096
        if len(chunk) > 4096:
            chunk = chunk[:4096]
        await update.message.reply_text(chunk)


async def _send_analysis(update: Update, analysis: str) -> None:
    """Send analysis as plain text, splitting if too long."""
    await _send_chunks(update, analysis)


async def _send_start(update: Update) -> None:
    """Send start/help message."""
    try:
        await update.message.reply_text(START_TEXT, parse_mode="Markdown")
    except Exception as e:
        logger.warning("Markdown failed for start, sending plain: %s", e)
        await update.message.reply_text(
            "Dream Recording & Analysis\n\n"
            "Record your dream right after waking — voice or text.\n\n"
            "Voice: send a voice message → transcript → analysis\n"
            "Text: write the dream → analysis\n\n"
            "You get: Place, Events, Participants, patterns, existential questions"
        )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await _send_start(update)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await _send_start(update)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice message: download → ASR → LLM/keyword analysis."""
    if not update.message or not update.message.voice:
        return

    await update.message.chat.send_action(ChatAction.TYPING)
    settings = get_settings()

    # Download voice file
    voice = update.message.voice
    tg_file = await context.bot.get_file(voice.file_id)
    audio_bytes = await tg_file.download_as_bytearray()
    audio_bytes = bytes(audio_bytes)

    # Transcribe
    transcript = asr_transcribe(
        audio_bytes=audio_bytes,
        base_url=settings.LOCAL_AI_ASR_BASE_URL,
        content_type="audio/ogg",
        timeout=settings.LOCAL_AI_ASR_TIMEOUT,
    )

    if not transcript:
        logger.warning("ASR returned empty transcript")
        await update.message.reply_text(
            "Could not transcribe the voice message. Check ASR service (port 8001)."
        )
        return

    # Send full transcript in chunks (voice can be up to ~10 min)
    await _send_chunks(update, f"Transcript:\n\n{transcript}")

    # Analyze
    await update.message.chat.send_action(ChatAction.TYPING)
    system_prompt = _load_system_prompt()

    analysis = llm_analyze(
        text=transcript,
        system_prompt=system_prompt,
        use_openrouter=settings.USE_OPENROUTER,
        openrouter_api_key=settings.OPENROUTER_API_KEY,
        openrouter_model=settings.OPENROUTER_MODEL,
        local_base_url=settings.LOCAL_AI_LLM_BASE_URL,
        timeout=settings.LOCAL_AI_LLM_TIMEOUT,
    )

    if analysis:
        await _send_analysis(update, analysis)
    else:
        fallback = analyze_dream_keywords(transcript)
        await _send_analysis(update, fallback + "\n\n(LLM unavailable, used keyword analysis)")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text message: LLM or keyword analysis."""
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    if not text:
        return

    await update.message.chat.send_action(ChatAction.TYPING)
    settings = get_settings()
    system_prompt = _load_system_prompt()

    analysis = llm_analyze(
        text=text,
        system_prompt=system_prompt,
        use_openrouter=settings.USE_OPENROUTER,
        openrouter_api_key=settings.OPENROUTER_API_KEY,
        openrouter_model=settings.OPENROUTER_MODEL,
        local_base_url=settings.LOCAL_AI_LLM_BASE_URL,
        timeout=settings.LOCAL_AI_LLM_TIMEOUT,
    )

    if analysis:
        await _send_analysis(update, analysis)
    else:
        fallback = analyze_dream_keywords(text)
        await _send_analysis(update, fallback + "\n\n(LLM unavailable, used keyword analysis)")
