import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from backend.main import app as fastapi_app


async def app(scope, receive, send):
    if scope.get("type") == "http":
        path = scope.get("path", "")
        if path.startswith("/api"):
            scope = {**scope, "path": path[4:] or "/"}

    await fastapi_app(scope, receive, send)
