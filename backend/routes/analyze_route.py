from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from pipeline.inference import InferenceService

router = APIRouter()


class AnalyzeRequest(BaseModel):
    text: str


def _resolve_risk_level(dark_ratio: float) -> str:
    if dark_ratio >= 60:
        return "High"
    if dark_ratio >= 25:
        return "Medium"
    return "Low"


@router.post("/analyze")
def analyze_text(payload: AnalyzeRequest, request: Request) -> dict:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    service: InferenceService = request.app.state.inference_service
    return service.predict(text)


@router.post("/detect-from-text")
def detect_from_text(payload: AnalyzeRequest, request: Request) -> dict:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    service: InferenceService = request.app.state.inference_service
    prediction_result = service.predict(text)

    detected_texts = []
    if prediction_result["prediction"] == 1:
        detected_texts.append(
            {
                "text": text,
                "confidence": prediction_result["confidence"],
            }
        )

    total_contents_scanned = 1
    total_dark_patterns_detected = 1 if prediction_result["prediction"] == 1 else 0
    dark_ratio = round((total_dark_patterns_detected / total_contents_scanned) * 100, 2)

    return {
        "total_contents_scanned": total_contents_scanned,
        "total_dark_patterns_detected": total_dark_patterns_detected,
        "dark_ratio": dark_ratio,
        "risk_level": _resolve_risk_level(dark_ratio),
        "detected_texts": detected_texts,
    }
