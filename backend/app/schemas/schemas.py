"""
Pydantic request/response schemas for API validation.
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, AnyHttpUrl


class PredictionRequest(BaseModel):
    """Request model for text prediction."""

    text: str = Field(..., min_length=1, max_length=2000, description="Text to analyze")
    explain: bool = Field(default=True, description="Include explanation in response")


class PredictionResponse(BaseModel):
    """Response model for prediction."""

    text: str
    is_dark_pattern: bool
    confidence: float
    pattern_type: Optional[str] = None
    pattern_confidence: Optional[float] = None
    explanation: Optional[dict] = None


class URLScanRequest(BaseModel):
    """Request model for URL scanning."""

    url: AnyHttpUrl = Field(..., description="URL to scan")
    explain: bool = Field(default=True, description="Include explanations")


class URLScanResponse(BaseModel):
    """Response model for URL scan."""

    url: str
    dark_patterns_detected: int
    risk_score: float
    categories: dict[str, int]
    elements_scanned: int


class AnalyticsRequest(BaseModel):
    """Request model for analytics data."""

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pattern_type: Optional[str] = None


class AnalyticsResponse(BaseModel):
    """Response model for analytics."""

    total_predictions: int
    dark_patterns_count: int
    accuracy_rate: float
    most_common_patterns: list[tuple[str, int]]
    predictions_by_date: dict[str, int]


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    model_loaded: bool
    database_connected: bool
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response."""

    status: str = "error"
    message: str
    error_code: str
    details: Optional[dict] = None
