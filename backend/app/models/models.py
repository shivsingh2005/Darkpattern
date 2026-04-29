"""
Database models for predictions and analytics.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, Index
from sqlalchemy.orm import Mapped

from backend.app.models.base import Base


class Prediction(Base):
    """Model for storing prediction history."""

    __tablename__ = "predictions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_dark_pattern = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)
    pattern_type = Column(String(100), nullable=True)
    pattern_confidence = Column(Float, nullable=True)
    explanation = Column(Text, nullable=True)
    user_feedback = Column(String(10), nullable=True)  # 'helpful', 'not_helpful', None
    source = Column(String(50), default="api")  # 'api', 'web', 'extension'
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_predictions_created_at", "created_at"),
        Index("ix_predictions_is_dark_pattern", "is_dark_pattern"),
        Index("ix_predictions_pattern_type", "pattern_type"),
    )


class URLScan(Base):
    """Model for storing URL scan results."""

    __tablename__ = "url_scans"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), nullable=False, index=True)
    dark_patterns_detected = Column(Integer, default=0)
    urgency_count = Column(Integer, default=0)
    scarcity_count = Column(Integer, default=0)
    misdirection_count = Column(Integer, default=0)
    obstruction_count = Column(Integer, default=0)
    sneaking_count = Column(Integer, default=0)
    social_proof_count = Column(Integer, default=0)
    forced_action_count = Column(Integer, default=0)
    total_elements_scanned = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)
    results = Column(Text, nullable=True)  # JSON string
    user_feedback = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_url_scans_url", "url"),
        Index("ix_url_scans_created_at", "created_at"),
    )


class APIKey(Base):
    """Model for managing API keys."""

    __tablename__ = "api_keys"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelPerformance(Base):
    """Model for tracking model performance metrics."""

    __tablename__ = "model_performance"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(50), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_model_performance_model_version", "model_version"),)
