from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

_inference_service = None

def get_inference_service():
    global _inference_service
    if _inference_service is None:
        try:
            from backend.pipeline.inference import InferenceService
            _inference_service = InferenceService()
            logger.info("✅ InferenceService initialized successfully")
        except FileNotFoundError as e:
            logger.error(f"❌ Model files not found: {e}")
            raise RuntimeError(f"Model artifacts missing: {e}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize InferenceService: {e}", exc_info=True)
            raise RuntimeError(f"InferenceService initialization failed: {e}")
    return _inference_service


def _cors_origins() -> list[str]:
    raw_origins = os.getenv("CORS_ORIGINS", "*")
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("🚀 Starting up application...")
        app.state.inference_service = get_inference_service()
        logger.info("✅ Application startup complete")
    except Exception as e:
        logger.critical(f"💥 STARTUP FAILED: {e}", exc_info=True)
        raise
    yield
    logger.info("🛑 Shutting down application...")

app = FastAPI(title="Dark Pattern Detection API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from backend.routes.analyze_route import router as analyze_router
    from backend.routes.url_route import router as url_router
    app.include_router(analyze_router)
    app.include_router(url_router)
    logger.info("✅ Routers loaded successfully")
except ImportError as e:
    logger.error(f"❌ Error importing routers: {e}", exc_info=True)
    raise

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
    first_error = exc.errors()[0] if exc.errors() else None
    message = first_error.get("msg", "Invalid request payload") if first_error else "Invalid request payload"
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": message},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": detail},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("❌ Unhandled server error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"},
    )

@app.get("/")
def health_check() -> dict:
    service_status = "loaded" if _inference_service is not None else "not loaded"
    return {
        "message": "Dark Pattern Detection API",
        "status": "running",
        "inference_service": service_status,
    }