"""Bot configuration via pydantic-settings."""

import logging
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Bot and service configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    TELEGRAM_BOT_TOKEN: str
    LOCAL_AI_ASR_BASE_URL: str = "http://localhost:8001"
    LOCAL_AI_LLM_BASE_URL: str = "http://localhost:8005"
    LOCAL_AI_ASR_TIMEOUT: int = 60
    LOCAL_AI_LLM_TIMEOUT: int = 60

    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    USE_OPENROUTER: bool = False

    @field_validator("TELEGRAM_BOT_TOKEN")
    @classmethod
    def token_not_empty(cls, v: str) -> str:
        if not v or v.strip() in ("", "your_bot_token"):
            raise ValueError("TELEGRAM_BOT_TOKEN is required and must not be placeholder")
        return v.strip()

    def validate_openrouter(self) -> None:
        """Ensure OpenRouter config is valid when USE_OPENROUTER is True."""
        if self.USE_OPENROUTER and not self.OPENROUTER_API_KEY:
            raise ValueError(
                "USE_OPENROUTER is True but OPENROUTER_API_KEY is not set"
            )


@lru_cache
def get_settings() -> Settings:
    """Load and validate settings (cached)."""
    settings = Settings()
    settings.validate_openrouter()
    return settings
