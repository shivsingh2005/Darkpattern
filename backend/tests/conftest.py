"""
Test configuration and fixtures.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DEBUG"] = "true"
os.environ["REQUIRE_API_KEY"] = "false"

from backend.app.models.base import Base
from backend.app.database.db import get_db
from backend.main import app


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_inference_service(monkeypatch):
    """Mock inference service."""

    class MockInferenceService:
        def predict(self, text: str) -> dict:
            return {"prediction": 0, "confidence": 0.95}

        def predict_batch(self, texts: list[str]) -> list[dict]:
            return [{"text": t, "prediction": 0, "confidence": 0.95} for t in texts]

    monkeypatch.setattr(
        "backend.app.api.dependencies.InferenceService",
        MockInferenceService,
    )
