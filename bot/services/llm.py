"""LLM client for dream analysis (port 8005 or OpenRouter)."""

import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


def analyze_dream(
    text: str,
    system_prompt: str,
    *,
    use_openrouter: bool = False,
    openrouter_api_key: Optional[str] = None,
    openrouter_model: str = "openai/gpt-4o-mini",
    local_base_url: Optional[str] = None,
    timeout: int = 60,
) -> Optional[str]:
    """
    Analyze dream text using LLM.

    Uses local LLM (8005) by default, or OpenRouter when use_openrouter=True
    and openrouter_api_key is set.

    Returns:
        Analysis text or None on failure
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]

    if use_openrouter and openrouter_api_key:
        return _call_openrouter(
            messages=messages,
            api_key=openrouter_api_key,
            model=openrouter_model,
            timeout=timeout,
        )

    if not local_base_url:
        logger.error("Local LLM base URL not configured")
        return None

    return _call_local(
        messages=messages,
        base_url=local_base_url,
        timeout=timeout,
    )


def _call_local(
    messages: list[dict],
    base_url: str,
    timeout: int,
) -> Optional[str]:
    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    payload = {
        "model": "default",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 1024,
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content")
            return content.strip() if content else None
    except httpx.ConnectError as e:
        logger.warning("LLM connection error: %s", e, extra={"base_url": base_url})
        return None
    except httpx.TimeoutException:
        logger.error("LLM request timed out")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(
            "LLM HTTP error: %s %s",
            e.response.status_code,
            e.response.text[:200],
        )
        return None
    except Exception as e:
        logger.exception("LLM unexpected error: %s", e)
        return None


def _call_openrouter(
    messages: list[dict],
    api_key: str,
    model: str,
    timeout: int,
) -> Optional[str]:
    url = f"{OPENROUTER_BASE}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 1024,
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/human-dream-dataset",
                },
            )
            response.raise_for_status()
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content")
            return content.strip() if content else None
    except httpx.HTTPStatusError as e:
        logger.error(
            "OpenRouter HTTP error: %s %s",
            e.response.status_code,
            e.response.text[:200],
        )
        return None
    except Exception as e:
        logger.exception("OpenRouter unexpected error: %s", e)
        return None
