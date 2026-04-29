"""
Application configuration using Pydantic v2 BaseSettings.
Supports environment-specific configuration with validation.
"""

import os
from typing import Optional

from pydantic import Field, HttpUrl, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration."""

    url: str = Field(
        default="sqlite:///./darkpattern.db",
        description="Database connection URL",
    )
    echo: bool = Field(default=False, description="Enable SQL query logging")
    pool_size: int = Field(default=20, description="Database connection pool size")
    max_overflow: int = Field(default=10, description="Maximum pool overflow")


class SecuritySettings(BaseSettings):
    """Security configuration."""

    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    api_keys: list[str] = Field(default_factory=list, description="List of valid API keys")
    secret_key: str = Field(default="your-secret-key-change-in-production", description="Secret key for signing")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration")
    require_api_key: bool = Field(default=False, description="Require API key for all endpoints")


class CORSSettings(BaseSettings):
    """CORS configuration."""

    origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )
    allow_credentials: bool = Field(default=True, description="Allow credentials in CORS")
    allow_methods: list[str] = Field(default=["*"], description="Allowed HTTP methods")
    allow_headers: list[str] = Field(default=["*"], description="Allowed headers")


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""

    enabled: bool = Field(default=True, description="Enable rate limiting")
    requests_per_minute: int = Field(default=60, description="Requests per minute limit")
    requests_per_hour: int = Field(default=1000, description="Requests per hour limit")


class LoggingSettings(BaseSettings):
    """Logging configuration."""

    level: str = Field(default="INFO", description="Log level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
    )
    file: Optional[str] = Field(default=None, description="Log file path")
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")


class MLSettings(BaseSettings):
    """Machine learning model configuration."""

    model_path: Optional[str] = Field(default=None, description="Path to model file")
    vectorizer_path: Optional[str] = Field(default=None, description="Path to vectorizer file")
    model_version: str = Field(default="1.0.0", description="Model version")
    cache_predictions: bool = Field(default=True, description="Cache prediction results")
    cache_ttl_seconds: int = Field(default=3600, description="Cache time-to-live")
    batch_size: int = Field(default=32, description="Batch prediction size")


class Settings(BaseSettings):
    """Main application settings."""

    # Application
    app_name: str = Field(default="Dark Pattern Detection API", description="Application name")
    app_version: str = Field(default="2.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment (dev/staging/prod)")
    debug: bool = Field(default=False, description="Debug mode")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=4, description="Number of workers")
    reload: bool = Field(default=True, description="Reload on code changes")

    # Services
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    rate_limit: RateLimitSettings = Field(default_factory=RateLimitSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    ml: MLSettings = Field(default_factory=MLSettings)

    # Optional integrations
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API key")
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False

    @validator("cors")
    def validate_cors_origins(cls, v: CORSSettings) -> CORSSettings:
        """Validate CORS origins."""
        if not v.origins or v.origins == ["*"]:
            if os.getenv("ENVIRONMENT") == "production":
                raise ValueError("Wildcard CORS origins not allowed in production")
        return v

    @validator("security")
    def validate_security_settings(cls, v: SecuritySettings) -> SecuritySettings:
        """Validate security settings."""
        if os.getenv("ENVIRONMENT") == "production":
            if v.secret_key == "your-secret-key-change-in-production":
                raise ValueError("Secret key must be changed in production")
        return v


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
