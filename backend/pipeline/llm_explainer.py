import asyncio
import json
import os
import re
from typing import Any

SYSTEM_INSTRUCTION = """
You are a dark pattern detection expert. You will be given text from a website
that has been classified as a dark pattern. Analyze it and respond ONLY with
valid JSON - no markdown, no code fences, no extra text whatsoever.
""".strip()


def _fallback_explanation(text: str, category: str, confidence: float) -> dict[str, str]:
    return {
        "why": f"This text uses {category} tactics to manipulate user behaviour.",
        "psychological_mechanism": "Exploits cognitive biases to bypass rational decision-making.",
        "harm": "Users may make decisions against their own interests.",
        "ethical_alternative": "Present the same information clearly without pressure or manipulation.",
    }


def _strip_code_fences(raw_text: str) -> str:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_json_response(raw_text: str) -> dict[str, str]:
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
    import google.generativeai as genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

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
        raise RuntimeError("Gemini returned an empty response")

    return text


async def explain_dark_pattern(text: str, category: str, confidence: float) -> dict[str, Any]:
    fallback = _fallback_explanation(text=text, category=category, confidence=confidence)

    if not os.environ.get("GEMINI_API_KEY"):
        return fallback

    user_message = (
        f"This text was detected as a \"{category}\" dark pattern \n"
        f"(confidence: {confidence:.0%}):\n\n"
        f"\"{text}\"\n\n"
        "Respond with exactly this JSON structure:\n"
        "{\n"
        "  \"why\": \"one sentence explaining why this specific text is a dark pattern\",\n"
        "  \"psychological_mechanism\": \"one sentence on the specific cognitive bias or psychological trick it exploits\",\n"
        "  \"harm\": \"one sentence on the concrete harm caused to the user\",\n"
        "  \"ethical_alternative\": \"rewrite this text ethically without the dark pattern\"\n"
        "}"
    )

    try:
        raw_response = await asyncio.to_thread(_generate_explanation_sync, user_message)
        return _parse_json_response(raw_response)
    except (json.JSONDecodeError, ValueError, RuntimeError):
        return fallback
    except Exception:
        return fallback
