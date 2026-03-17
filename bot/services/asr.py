"""ASR client for voice transcription (port 8001)."""

import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

ASR_MODEL = "cstr/whisper-large-v3-turbo-int8_float32"


def transcribe(
    audio_bytes: bytes,
    base_url: str,
    content_type: str = "audio/ogg",
    timeout: int = 60,
) -> Optional[str]:
    """
    Transcribe audio using remote ASR service.

    Args:
        audio_bytes: Raw audio data
        base_url: ASR service base URL (e.g. http://host:8001)
        content_type: MIME type (e.g. audio/ogg for Telegram voice)
        timeout: Request timeout in seconds

    Returns:
        Transcribed text or None on failure
    """
    url = f"{base_url.rstrip('/')}/v1/audio/transcriptions"

    files = {"file": ("voice.ogg", audio_bytes, content_type)}
    data = {"model": ASR_MODEL}

    for attempt in range(2):
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(url, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                text = result.get("text", "").strip()
                return text if text else None
        except httpx.ConnectError as e:
            logger.warning(
                "ASR connection error (attempt %d): %s",
                attempt + 1,
                e,
                extra={"base_url": base_url},
            )
            if attempt == 1:
                logger.error("ASR service unavailable after retry")
                return None
        except httpx.TimeoutException:
            logger.error("ASR request timed out")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(
                "ASR HTTP error: %s %s",
                e.response.status_code,
                e.response.text[:200],
            )
            return None
        except Exception as e:
            logger.exception("ASR unexpected error: %s", e)
            return None

    return None
