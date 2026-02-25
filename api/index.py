from pathlib import Path
import sys
import logging

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
    logger.info("Successfully imported FastAPI app")
except Exception as e:
    logger.error(f"Import error: {e}", exc_info=True)
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