"""
API router registration and configuration.
"""

from fastapi import APIRouter

from backend.app.api.routes import health, analyze, scan, analytics


def get_api_router() -> APIRouter:
    """Create and configure API router."""
    api_router = APIRouter()

    # Include route modules
    api_router.include_router(health.router)
    api_router.include_router(analyze.router)
    api_router.include_router(scan.router)
    api_router.include_router(analytics.router)

    return api_router
