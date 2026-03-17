#!/usr/bin/env python3
"""Telegram bot for dream recording and analysis."""

import logging
import sys

from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.config import get_settings
from bot.handlers import cmd_start, cmd_help, handle_text, handle_voice

logging.basicConfig(
    format="%(asctime)s · %(levelname)s · %(name)s · %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Set bot command menu (visible when user taps /)."""
    await application.bot.set_my_commands([
        BotCommand("start", "Start / show instructions"),
        BotCommand("help", "Repeat instructions"),
    ])


def main() -> None:
    settings = get_settings()

    application = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Starting Dream Bot (ASR: %s, LLM: %s)", settings.LOCAL_AI_ASR_BASE_URL, settings.LOCAL_AI_LLM_BASE_URL)
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
