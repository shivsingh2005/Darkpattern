"""
LLM-powered explanation generator for dark patterns.
"""

import asyncio
import json
import logging
import os
import re
from typing import Any, Optional


logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
You are a dark pattern detection expert. Analyze the given text classified as a dark pattern
and respond ONLY with valid JSON - no markdown, no code fences, no extra text whatsoever.
""".strip()


def _fallback_explanation(text: str, category: str, confidence: float) -> dict[str, str]:
    """Generate fallback explanation without LLM."""
    return {
        "why": f"This text uses {category} tactics to manipulate user behavior.",
        "psychological_mechanism": "Exploits cognitive biases to bypass rational decision-making.",
        "harm": "Users may make decisions against their own interests.",
        "ethical_alternative": "Present the same information clearly without pressure or manipulation.",
    }


def _strip_code_fences(raw_text: str) -> str:
    """Strip markdown code fences from response."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_json_response(raw_text: str) -> dict[str, str]:
    """Parse and validate JSON response."""
    cleaned = _strip_code_fences(raw_text)
    parsed = json.loads(cleaned)

    if not isinstance(parsed, dict):
        raise ValueError("LLM response is not a JSON object")

    required_keys = ["why", "psychological_mechanism", "harm", "ethical_alternative"]
    result: dict[str, str] = {}

    for key in required_keys:
        value = parsed.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"LLM response missing or invalid key: {key}")
        result[key] = value.strip()

    return result


def _generate_explanation_sync(user_message: str) -> str:
    """Generate explanation using Gemini API synchronously."""
    try:
        import google.generativeai as genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            [
                {"role": "user", "parts": [SYSTEM_INSTRUCTION]},
                {"role": "user", "parts": [user_message]},
            ],
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned empty response")

        return text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


async def explain_dark_pattern(
    text: str,
    category: str,
    confidence: float,
) -> dict[str, Any]:
    """
    Generate explanation for dark pattern using LLM.

    Args:
        text: Text that was identified as dark pattern
        category: Category of dark pattern
        confidence: Confidence score

    Returns:
        Dictionary with explanation
    """
    fallback = _fallback_explanation(text=text, category=category, confidence=confidence)

    if not os.environ.get("GEMINI_API_KEY"):
        return fallback

    try:
        user_message = (
            f'This text was detected as a "{category}" dark pattern '
            f"(confidence: {confidence:.0%}):\n\n"
            f'"{text}"\n\n'
            "Respond with exactly this JSON structure:\n"
            '{"why": "...", "psychological_mechanism": "...", "harm": "...", '
            '"ethical_alternative": "..."}'
        )

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response_text = await loop.run_in_executor(
            None, _generate_explanation_sync, user_message
        )

        parsed = _parse_json_response(response_text)
        return {
            **parsed,
            "confidence": confidence,
            "category": category,
        }

    except Exception as e:
        logger.warning(f"LLM explanation failed, using fallback: {e}")
        return fallback
