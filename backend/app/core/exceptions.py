"""
Custom exception classes for the application.
"""

from typing import Any, Optional


class ApplicationError(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(ApplicationError):
    """Validation error."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class AuthenticationError(ApplicationError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(ApplicationError):
    """Authorization error."""

    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
        )


class ResourceNotFoundError(ApplicationError):
    """Resource not found error."""

    def __init__(self, resource_type: str, resource_id: Any):
        super().__init__(
            message=f"{resource_type} not found: {resource_id}",
            error_code="NOT_FOUND",
            status_code=404,
        )


class ConflictError(ApplicationError):
    """Conflict error."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
        )


class RateLimitError(ApplicationError):
    """Rate limit exceeded error."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )


class ServiceUnavailableError(ApplicationError):
    """Service unavailable error."""

    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(
            message=message,
            error_code="SERVICE_UNAVAILABLE",
            status_code=503,
        )


class ModelError(ApplicationError):
    """Model-related error."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="MODEL_ERROR",
            status_code=500,
            details=details,
        )


class DatabaseError(ApplicationError):
    """Database-related error."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
            details=details,
        )


class ExternalServiceError(ApplicationError):
    """External service error (e.g., Gemini API)."""

    def __init__(self, service_name: str, message: str):
        super().__init__(
            message=f"{service_name} error: {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=503,
        )
