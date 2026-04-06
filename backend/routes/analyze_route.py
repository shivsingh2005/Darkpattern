import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from backend.pipeline.inference import InferenceService
from backend.pipeline.llm_explainer import explain_dark_pattern
from backend.pipeline.type_classifier import predict_type

router = APIRouter()
logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    text: str
    explain: bool = True


def _validated_text(raw_text: str) -> str:
    text = raw_text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(text) < 3:
        raise HTTPException(status_code=400, detail="Text must be at least 3 characters")
    if len(text) > 2000:
        raise HTTPException(status_code=400, detail="Text must be at most 2000 characters")
    return text


def _get_inference_service(request: Request) -> InferenceService:
    service = getattr(request.app.state, "inference_service", None)
    if service is None:
        service = InferenceService()
        request.app.state.inference_service = service
    return service


@router.post("/analyze")
async def analyze_text(payload: AnalyzeRequest, request: Request) -> dict:
    text = _validated_text(payload.text)

    service = _get_inference_service(request)
    try:
        binary_result = service.predict(text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Layer 1 failed: {exc}") from exc

    is_dark_pattern = bool(binary_result.get("prediction") == 1)
    binary_confidence = float(binary_result.get("confidence", 0.0))

    type_result = None
    explanation = None

    if is_dark_pattern:
        try:
            type_result = predict_type(text)
        except Exception as exc:
            logger.error("Layer 2 failed: %s", exc, exc_info=True)
            type_result = None

        if payload.explain:
            try:
                category = type_result["category"] if type_result else "Unknown"
                category_confidence = type_result["confidence"] if type_result else binary_confidence
                explanation = await explain_dark_pattern(text, category, category_confidence)
            except Exception as exc:
                logger.error("Layer 3 failed: %s", exc, exc_info=True)
                explanation = None

    return {
        "text": text,
        "is_dark_pattern": is_dark_pattern,
        "binary_confidence": binary_confidence,
        "type": type_result,
        "explanation": explanation,
    }


@router.post("/detect-from-text")
async def detect_from_text(payload: AnalyzeRequest, request: Request) -> dict:
    return await analyze_text(payload, request)
