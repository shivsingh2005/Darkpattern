from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from backend.main import app as fastapi_app


async def app(scope, receive, send):
    if scope.get("type") == "http":
        path = scope.get("path", "")
        if path.startswith("/api"):
            stripped = path[4:] or "/"
            scope = {**scope, "path": stripped}

    await fastapi_app(scope, receive, send)
