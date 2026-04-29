"""
Health check and diagnostic endpoints.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Request

from backend.app.core.config import settings
from backend.app.schemas.schemas import HealthCheckResponse, ErrorResponse


logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheckResponse, status_code=200)
async def health_check(request: Request) -> HealthCheckResponse:
    """
    Health check endpoint.

    Returns:
        HealthCheckResponse with service status
    """
    model_loaded = hasattr(request.app.state, "inference_service")
    database_connected = True  # TODO: Add actual DB connection check

    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        model_loaded=model_loaded,
        database_connected=database_connected,
        timestamp=datetime.utcnow(),
    )


@router.get("/metrics", tags=["monitoring"])
async def metrics() -> dict:
    """
    Get service metrics.

    Returns:
        Dictionary with service metrics
    """
    return {
        "status": "available",
        "requests_total": 0,
        "requests_error": 0,
        "avg_response_time_ms": 0,
    }
