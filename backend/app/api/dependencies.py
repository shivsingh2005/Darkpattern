"""
API route dependencies.
"""

import logging
from fastapi import Depends, Request

from backend.app.ml.inference import InferenceService
from backend.app.core.security import validate_api_key


logger = logging.getLogger(__name__)


def get_inference_service(request: Request) -> InferenceService:
    """
    Get or create inference service from app state.

    Args:
        request: FastAPI request object

    Returns:
        InferenceService instance
    """
    if not hasattr(request.app.state, "inference_service"):
        request.app.state.inference_service = InferenceService()
    return request.app.state.inference_service


async def get_current_api_key(api_key: str = Depends(validate_api_key)) -> str:
    """
    Get current API key from request.

    Args:
        api_key: API key from dependency

    Returns:
        API key string
    """
    return api_key
