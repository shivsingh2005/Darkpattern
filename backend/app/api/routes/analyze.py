"""
Text analysis endpoints.
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Depends

from backend.app.schemas.schemas import PredictionRequest, PredictionResponse
from backend.app.api.dependencies import get_inference_service, get_current_api_key
from backend.app.ml.type_classifier import predict_type
from backend.app.ml.llm_explainer import explain_dark_pattern
from backend.app.core.security import sanitize_text_input
from backend.app.core.exceptions import ValidationError, ModelError


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post("/analyze", response_model=PredictionResponse)
async def analyze_text(
    request: PredictionRequest,
    http_request: Request,
    api_key: str = Depends(get_current_api_key),
) -> PredictionResponse:
    """
    Analyze text for dark patterns.

    Args:
        request: Analysis request with text
        http_request: FastAPI request
        api_key: Validated API key

    Returns:
        Prediction response with confidence and type
    """
    try:
        # Validate input
        text = sanitize_text_input(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        # Get inference service
        service = get_inference_service(http_request)

        # Binary classification
        binary_result = service.predict(text)
        is_dark_pattern = bool(binary_result.get("prediction") == 1)
        binary_confidence = float(binary_result.get("confidence", 0.0))

        pattern_type = None
        pattern_confidence = None
        explanation = None

        # Multi-class classification if dark pattern detected
        if is_dark_pattern:
            try:
                type_result = predict_type(text)
                pattern_type = type_result.get("category")
                pattern_confidence = type_result.get("confidence")
            except Exception as e:
                logger.error(f"Type classification failed: {e}")

            # Generate explanation if requested
            if request.explain and pattern_type:
                try:
                    explanation = await explain_dark_pattern(
                        text, pattern_type, pattern_confidence or binary_confidence
                    )
                except Exception as e:
                    logger.error(f"Explanation generation failed: {e}")

        return PredictionResponse(
            text=text,
            is_dark_pattern=is_dark_pattern,
            confidence=binary_confidence,
            pattern_type=pattern_type,
            pattern_confidence=pattern_confidence,
            explanation=explanation,
        )

    except ModelError as e:
        logger.error(f"Model error: {e}")
        raise HTTPException(status_code=500, detail="Model inference failed")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/analyze/batch")
async def analyze_batch(
    texts: list[str],
    http_request: Request,
    api_key: str = Depends(get_current_api_key),
) -> dict:
    """
    Analyze multiple texts in batch.

    Args:
        texts: List of texts to analyze
        http_request: FastAPI request
        api_key: Validated API key

    Returns:
        List of predictions
    """
    if not texts or len(texts) > 100:
        raise HTTPException(
            status_code=400,
            detail="Provide 1-100 texts for batch analysis",
        )

    try:
        service = get_inference_service(http_request)
        results = service.predict_batch(texts)

        return {
            "total": len(results),
            "results": results,
        }
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Batch analysis failed")
