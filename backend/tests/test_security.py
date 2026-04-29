"""
Security utilities tests.
"""

import pytest

from backend.app.core.security import (
    sanitize_text_input,
    sanitize_url,
    hash_string,
    constant_time_compare,
)


def test_sanitize_text_valid():
    """Test sanitizing valid text."""
    text = "This is valid text"
    result = sanitize_text_input(text)
    assert result == text


def test_sanitize_text_empty():
    """Test sanitizing empty text."""
    with pytest.raises(ValueError):
        sanitize_text_input("")


def test_sanitize_text_whitespace():
    """Test sanitizing whitespace-only text."""
    with pytest.raises(ValueError):
        sanitize_text_input("   ")


def test_sanitize_text_too_long():
    """Test sanitizing text exceeding max length."""
    text = "a" * 2001
    with pytest.raises(ValueError):
        sanitize_text_input(text, max_length=2000)


def test_sanitize_text_null_bytes():
    """Test sanitizing text with null bytes."""
    text = "Valid\x00Invalid"
    with pytest.raises(ValueError):
        sanitize_text_input(text)


def test_sanitize_url_valid():
    """Test sanitizing valid URL."""
    url = "https://example.com"
    result = sanitize_url(url)
    assert result == url


def test_sanitize_url_http():
    """Test sanitizing HTTP URL."""
    url = "http://example.com"
    result = sanitize_url(url)
    assert result == url


def test_sanitize_url_no_protocol():
    """Test sanitizing URL without protocol."""
    with pytest.raises(ValueError):
        sanitize_url("example.com")


def test_sanitize_url_empty():
    """Test sanitizing empty URL."""
    with pytest.raises(ValueError):
        sanitize_url("")


def test_hash_string_sha256():
    """Test SHA256 hashing."""
    text = "test"
    result = hash_string(text, algorithm="sha256")
    assert len(result) == 64  # SHA256 hex length
    # Verify hash is deterministic
    assert result == hash_string(text, algorithm="sha256")


def test_hash_string_sha512():
    """Test SHA512 hashing."""
    text = "test"
    result = hash_string(text, algorithm="sha512")
    assert len(result) == 128  # SHA512 hex length


def test_constant_time_compare_equal():
    """Test constant time comparison with equal strings."""
    assert constant_time_compare("test", "test")


def test_constant_time_compare_not_equal():
    """Test constant time comparison with different strings."""
    assert not constant_time_compare("test1", "test2")
