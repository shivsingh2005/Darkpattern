import asyncio
import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import AnyHttpUrl, BaseModel

from backend.pipeline.inference import InferenceService
from backend.pipeline.llm_explainer import explain_dark_pattern
from backend.pipeline.type_classifier import predict_type
from webscraper.scraper import ScraperBlockedError, ScraperTimeoutError, scrape_structured

router = APIRouter()
logger = logging.getLogger(__name__)

CATEGORIES = [
    "Forced Action",
    "Misdirection",
    "Obstruction",
    "Scarcity",
    "Sneaking",
    "Social Proof",
    "Urgency",
]

SOURCE_KEYS = [
    "urgency_scarcity",
    "timer_countdown",
    "popups_overlays",
    "cta_buttons",
    "checkout_price_text",
    "social_proof",
]


class URLRequest(BaseModel):
    url: AnyHttpUrl
    explain: bool = True


def _normalize_text(text: str) -> str:
    return " ".join(str(text).split()).strip()


def _init_summary() -> dict[str, int]:
    return {category: 0 for category in CATEGORIES}


def _get_inference_service(request: Request) -> InferenceService:
    service = getattr(request.app.state, "inference_service", None)
    if service is None:
        service = InferenceService()
        request.app.state.inference_service = service
    return service


def _build_tier_one(priority_elements: dict) -> list[dict]:
    seen: set[str] = set()
    queue: list[dict] = []

    for source in SOURCE_KEYS:
        values = priority_elements.get(source, []) if isinstance(priority_elements, dict) else []
        for raw_value in values:
            text = _normalize_text(raw_value)
            if len(text) < 8 or text in seen:
                continue
            seen.add(text)
            queue.append({"text": text, "source": source})

    return queue


def _build_tier_two(full_text: str, tier_one_texts: set[str]) -> list[dict]:
    queue: list[dict] = []
    seen = set(tier_one_texts)

    for line in str(full_text).splitlines():
        text = _normalize_text(line)
        if text in seen:
            continue
        if len(text) < 10 or len(text) > 500:
            continue
        seen.add(text)
        queue.append({"text": text, "source": None})
        if len(queue) >= 150:
            break

    return queue


async def _analyze_item(
    service: InferenceService,
    text: str,
    should_explain: bool,
) -> dict:
    try:
        binary_result = service.predict(text)
    except Exception as exc:
        logger.error("Layer 1 failed for URL text: %s", exc, exc_info=True)
        return {
            "text": text,
            "is_dark_pattern": False,
            "binary_confidence": 0.0,
            "type": None,
            "explanation": None,
        }

    is_dark_pattern = bool(binary_result.get("prediction") == 1)
    binary_confidence = float(binary_result.get("confidence", 0.0))

    if not is_dark_pattern:
        return {
            "text": text,
            "is_dark_pattern": False,
            "binary_confidence": binary_confidence,
            "type": None,
            "explanation": None,
        }

    type_result = None
    explanation = None

    try:
        type_result = predict_type(text)
    except Exception as exc:
        logger.error("Layer 2 failed for URL text: %s", exc, exc_info=True)
        type_result = None

    if should_explain:
        try:
            category = type_result["category"] if type_result else "Unknown"
            confidence = type_result["confidence"] if type_result else binary_confidence
            explanation = await explain_dark_pattern(text, category, confidence)
        except Exception as exc:
            logger.error("Layer 3 failed for URL text: %s", exc, exc_info=True)
            explanation = None

    return {
        "text": text,
        "is_dark_pattern": True,
        "binary_confidence": binary_confidence,
        "type": type_result,
        "explanation": explanation,
    }


@router.post("/detect-from-url")
async def detect_from_url(payload: URLRequest, request: Request) -> dict:
    url = str(payload.url)

    try:
        scraped = await asyncio.to_thread(scrape_structured, url)
    except ScraperBlockedError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ScraperTimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Scraper failed: {exc}") from exc

    if not isinstance(scraped, dict):
        raise HTTPException(status_code=503, detail="Scraper returned invalid response")

    priority_elements = scraped.get("priority_elements", {})
    tier_one = _build_tier_one(priority_elements)
    tier_one_texts = {item["text"] for item in tier_one}
    tier_two = _build_tier_two(scraped.get("full_text", ""), tier_one_texts)

    service = _get_inference_service(request)

    high_priority_findings = []
    results = []
    summary = _init_summary()

    for item in tier_one:
        analyzed = await _analyze_item(service, item["text"], should_explain=True)
        high_priority_findings.append({**analyzed, "source": item["source"]})
        results.append(analyzed)
        if analyzed["is_dark_pattern"] and analyzed["type"]:
            category = analyzed["type"].get("category")
            if category in summary:
                summary[category] += 1

    for item in tier_two:
        analyzed = await _analyze_item(service, item["text"], should_explain=payload.explain)
        results.append(analyzed)
        if analyzed["is_dark_pattern"] and analyzed["type"]:
            category = analyzed["type"].get("category")
            if category in summary:
                summary[category] += 1

    total_texts_scanned = len(results)
    dark_patterns_found = sum(1 for entry in results if entry["is_dark_pattern"])

    return {
        "url": scraped.get("url", url),
        "page_title": scraped.get("page_title", ""),
        "total_texts_scanned": total_texts_scanned,
        "dark_patterns_found": dark_patterns_found,
        "high_priority_findings": high_priority_findings,
        "results": results,
        "summary": summary,
    }
