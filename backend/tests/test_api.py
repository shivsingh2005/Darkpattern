"""
API endpoint tests.
"""

import pytest


def test_analyze_text_empty(client):
    """Test analyze with empty text."""
    response = client.post("/api/v1/analyze", json={"text": ""})
    assert response.status_code == 400


def test_analyze_text_too_short(client):
    """Test analyze with text too short."""
    response = client.post("/api/v1/analyze", json={"text": "a"})
    assert response.status_code == 400


def test_analyze_text_too_long(client):
    """Test analyze with text too long."""
    long_text = "a" * 2001
    response = client.post("/api/v1/analyze", json={"text": long_text})
    assert response.status_code == 400


def test_analyze_text_valid(client, mock_inference_service):
    """Test analyze with valid text."""
    response = client.post(
        "/api/v1/analyze",
        json={"text": "Buy now, limited time offer!", "explain": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "is_dark_pattern" in data
    assert "confidence" in data


def test_analyze_batch_empty(client):
    """Test batch analyze with empty list."""
    response = client.post("/api/v1/analyze/batch", json={"texts": []})
    assert response.status_code == 400


def test_analyze_batch_too_many(client):
    """Test batch analyze with too many texts."""
    texts = ["test"] * 101
    response = client.post("/api/v1/analyze/batch", json={"texts": texts})
    assert response.status_code == 400


def test_analyze_batch_valid(client, mock_inference_service):
    """Test batch analyze with valid texts."""
    texts = ["Buy now!", "Limited offer"]
    response = client.post("/api/v1/analyze/batch", json={"texts": texts})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == len(texts)
    assert len(data["results"]) == len(texts)


def test_scan_url_invalid(client):
    """Test URL scan with invalid URL."""
    response = client.post("/api/v1/scan-url", json={"url": "not-a-url"})
    assert response.status_code == 400


def test_scan_url_valid(client):
    """Test URL scan with valid URL."""
    response = client.post(
        "/api/v1/scan-url",
        json={"url": "https://example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "dark_patterns_detected" in data
    assert "risk_score" in data


def test_analytics_endpoint(client):
    """Test analytics endpoint."""
    response = client.get("/api/v1/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "dark_patterns_count" in data
    assert "accuracy_rate" in data
