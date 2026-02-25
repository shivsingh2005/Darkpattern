from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add backend to path for serverless environment
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

logger = logging.getLogger(__name__)

# Lazy import to handle serverless initialization
_inference_service = None

def get_inference_service():
    global _inference_service
    if _inference_service is None:
        try:
            from pipeline.inference import InferenceService
            _inference_service = InferenceService()
        except Exception as e:
            logger.error(f"Failed to initialize InferenceService: {e}")
            raise
    return _inference_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.inference_service = get_inference_service()
        logger.info("InferenceService initialized successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        app.state.inference_service = None
    yield

app = FastAPI(title="Dark Pattern Detection API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers after app is created
try:
    from routes.analyze_route import router as analyze_router
    from routes.url_route import router as url_router
    app.include_router(analyze_router)
    app.include_router(url_router)
except ImportError as e:
    logger.error(f"Error importing routers: {e}")

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
    logger.exception("Unhandled server error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"},
    )

@app.get("/")
def health_check() -> dict:
    return {"message": "Dark Pattern Detection API", "status": "running"}