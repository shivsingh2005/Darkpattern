"""
Main FastAPI application factory.
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging, logger as app_logger
from backend.app.core.exceptions import ApplicationError
from backend.app.database.db import init_db
from backend.app.ml.inference import InferenceService
from backend.app.api.routes.main import get_api_router


logger = logging.getLogger(__name__)


# Setup logging
setup_logging(
    level=settings.logging.level,
    log_file=settings.logging.file,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    try:
        app_logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
        
        # Initialize database
        init_db()
        app_logger.info("✅ Database initialized")

        # Load ML model
        app.state.inference_service = InferenceService()
        app_logger.info("✅ ML model loaded")

    except Exception as e:
        app_logger.critical(f"💥 Startup failed: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    app_logger.info("🛑 Shutting down application...")


def create_app() -> FastAPI:
    """
    Create FastAPI application instance.

    Returns:
        FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Advanced Dark Pattern Detection API",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Middleware - Order matters!

    # 1. Trusted Host
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],  # TODO: Restrict in production
    )

    # 2. GZIP Compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # 3. CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )

    # Exception handlers
    @app.exception_handler(ApplicationError)
    async def app_error_handler(request: Request, exc: ApplicationError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.message,
                "error_code": exc.error_code,
                "details": exc.details if settings.debug else None,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        first_error = exc.errors()[0] if exc.errors() else {}
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": first_error.get("msg", "Validation error"),
                "error_code": "VALIDATION_ERROR",
            },
        )

    @app.exception_handler(Exception)
    async def general_error_handler(request: Request, exc: Exception):
        app_logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error" if not settings.debug else str(exc),
                "error_code": "INTERNAL_ERROR",
            },
        )

    # Include routers
    api_router = get_api_router()
    app.include_router(api_router)

    # Root endpoint
    @app.get("/")
    async def root() -> dict:
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running",
            "docs": "/docs" if settings.debug else None,
        }

    return app


# Create app instance
app = create_app()