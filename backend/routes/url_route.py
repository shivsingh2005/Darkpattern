import sys
from pathlib import Path
import re
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from pipeline.inference import InferenceService

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from webscraper.scraper import WebScraper

router = APIRouter()


class URLRequest(BaseModel):
    url: str


def _is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").strip()
    if parsed.scheme not in {"http", "https"}:
        return False
    if not host or "." not in host:
        return False
    if len(host) > 253:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9.-]+", host))


def _resolve_risk_level(dark_ratio: float) -> str:
    if dark_ratio >= 60:
        return "High"
    if dark_ratio >= 25:
        return "Medium"
    return "Low"


def _normalize_chunk(text: str) -> str:
    return " ".join(text.split()).strip()


def _extract_chunks(scraper: WebScraper, url: str) -> list[str]:
    html = scraper.fetch(url)
    if html is None:
        raise HTTPException(status_code=400, detail="Failed to fetch URL content")

    soup = scraper.parse(html)
    if soup is None:
        raise HTTPException(status_code=400, detail="Failed to parse URL content")

    for node in soup(["script", "style"]):
        node.decompose()

    raw_chunks: list[str] = []

    for paragraph in soup.find_all("p"):
        text = _normalize_chunk(paragraph.get_text(" ", strip=True))
        if text:
            raw_chunks.append(text)

    for button in soup.find_all("button"):
        text = _normalize_chunk(button.get_text(" ", strip=True))
        if text:
            raw_chunks.append(text)

    for input_button in soup.find_all("input"):
        input_type = (input_button.get("type") or "").strip().lower()
        if input_type in {"button", "submit"}:
            value = _normalize_chunk(input_button.get("value") or "")
            if value:
                raw_chunks.append(value)

    if not raw_chunks:
        text = _normalize_chunk(soup.get_text(" ", strip=True))
        if text:
            raw_chunks.extend(re.split(r"(?<=[.!?])\s+", text))

    filtered_chunks: list[str] = []
    seen = set()
    for chunk in raw_chunks:
        cleaned = _normalize_chunk(chunk)
        if len(cleaned) < 15:
            continue
        if len(cleaned.split()) < 3:
            continue
        if len(cleaned) > 1200:
            cleaned = cleaned[:1200]
        if cleaned in seen:
            continue
        seen.add(cleaned)
        filtered_chunks.append(cleaned)

    if len(filtered_chunks) > 300:
        filtered_chunks = filtered_chunks[:300]

    return filtered_chunks


@router.post("/detect-from-url")
def detect_from_url(payload: URLRequest, request: Request) -> dict:
    url = _normalize_chunk(payload.url)
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
    if not _is_valid_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL. Use http:// or https://")

    scraper = WebScraper(timeout=15)
    chunks = _extract_chunks(scraper, url)
    if not chunks:
        raise HTTPException(status_code=400, detail="No usable visible text chunks found on page")

    service: InferenceService = request.app.state.inference_service
    predictions = service.predict_chunks(chunks)

    total_contents_scanned = len(predictions)
    detected = [
        {
            "text": item["text"],
            "confidence": item["confidence"],
        }
        for item in predictions
        if item["prediction"] == 1
    ]

    total_dark_patterns_detected = len(detected)
    dark_ratio = (
        round((total_dark_patterns_detected / total_contents_scanned) * 100, 2)
        if total_contents_scanned > 0
        else 0.0
    )

    return {
        "total_contents_scanned": total_contents_scanned,
        "total_dark_patterns_detected": total_dark_patterns_detected,
        "dark_ratio": dark_ratio,
        "risk_level": _resolve_risk_level(dark_ratio),
        "detected_texts": detected,
    }
