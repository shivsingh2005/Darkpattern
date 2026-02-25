from pathlib import Path
import sys
import logging
import platform
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

try:
    from backend.main import app as fastapi_app
    logger.info("✅ Successfully imported FastAPI app")
except Exception as e:
    logger.error("=" * 60)
    logger.error("💥 FAILED TO IMPORT FastAPI app")
    logger.error("=" * 60)
    logger.error(f"Error: {type(e).__name__}: {e}")
    logger.error(f"Python version: {platform.python_version()} ({platform.system()} {platform.machine()})")
    logger.error(f"Working directory: {Path.cwd()}")
    logger.error(f"This file: {Path(__file__).resolve()}")
    logger.error(f"PROJECT_ROOT: {PROJECT_ROOT}")
    logger.error(f"BACKEND_DIR: {BACKEND_DIR}")
    logger.error(f"sys.path: {sys.path}")
    # Check for model files at expected locations
    model_paths = [
        PROJECT_ROOT / "model" / "model.pkl",
        PROJECT_ROOT / "Model" / "model.pkl",
        PROJECT_ROOT / "model" / "vectorizer.pkl",
        PROJECT_ROOT / "Model" / "vectorizer.pkl",
    ]
    for mp in model_paths:
        logger.error(f"  Model file {mp}: {'EXISTS' if mp.exists() else 'MISSING'}")
    logger.error("Full traceback:")
    logger.error(traceback.format_exc())
    logger.error("=" * 60)
    fastapi_app = None


async def app(scope, receive, send):
    if fastapi_app is None:
        await send({
            "type": "http.response.start",
            "status": 500,
            "headers": [[b"content-type", b"application/json"]],
        })
        await send({
            "type": "http.response.body",
            "body": b'{"error": "Application failed to initialize"}',
        })
        return

    if scope.get("type") == "http":
        path = scope.get("path", "")
        if path.startswith("/api"):
            scope = {**scope, "path": path[4:] or "/"}

    await fastapi_app(scope, receive, send)