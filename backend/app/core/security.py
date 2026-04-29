"""
Security utilities including authentication, authorization, and input validation.
"""

import hashlib
import hmac
import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from backend.app.core.config import settings


logger = logging.getLogger(__name__)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class SecurityError(Exception):
    """Base security exception."""

    pass


class InvalidAPIKeyError(SecurityError):
    """Invalid API key error."""

    pass


def validate_api_key(api_key: Optional[str] = Depends(api_key_header)) -> str:
    """
    Validate API key from request header.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        Validated API key

    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not settings.security.require_api_key:
        return "anonymous"

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is required",
        )

    if not verify_api_key(api_key):
        logger.warning(f"Invalid API key attempt: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return api_key


def verify_api_key(api_key: str) -> bool:
    """
    Verify API key validity.

    Args:
        api_key: API key to verify

    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False

    # Check against configured API keys
    valid_keys = settings.security.api_keys
    if valid_keys and api_key not in valid_keys:
        return False

    # Check against environment variable
    env_key = settings.security.api_key
    if env_key and api_key != env_key:
        return False

    return True if (valid_keys or env_key) else True


def sanitize_text_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitize text input for security.

    Args:
        text: Text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text

    Raises:
        ValueError: If input is invalid
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Strip whitespace
    text = text.strip()

    # Check length
    if not text:
        raise ValueError("Input cannot be empty")
    if len(text) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length} characters")

    # Check for null bytes
    if "\x00" in text:
        raise ValueError("Input contains invalid characters")

    return text


def sanitize_url(url: str) -> str:
    """
    Sanitize URL input.

    Args:
        url: URL to sanitize

    Returns:
        Sanitized URL

    Raises:
        ValueError: If URL is invalid
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty")

    # Basic URL validation
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("URL must start with http:// or https://")

    if len(url) > 2048:
        raise ValueError("URL is too long")

    return url


def hash_string(value: str, algorithm: str = "sha256") -> str:
    """
    Hash a string value.

    Args:
        value: String to hash
        algorithm: Hashing algorithm (sha256, sha512, md5)

    Returns:
        Hashed string
    """
    if algorithm == "sha256":
        return hashlib.sha256(value.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(value.encode()).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(value.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def constant_time_compare(a: str, b: str) -> bool:
    """
    Constant time string comparison to prevent timing attacks.

    Args:
        a: First string
        b: Second string

    Returns:
        True if strings match, False otherwise
    """
    return hmac.compare_digest(a, b)
