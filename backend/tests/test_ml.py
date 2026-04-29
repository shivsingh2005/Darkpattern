"""
ML preprocessing and inference tests.
"""

import pytest

from backend.app.ml.preprocessing import preprocess_text, tokenize, chunk_text


def test_preprocess_text_basic():
    """Test basic text preprocessing."""
    text = "Hello, World!"
    result = preprocess_text(text, lemmatize=False)
    assert isinstance(result, str)
    assert result  # Not empty


def test_preprocess_text_lowercase():
    """Test lowercase conversion."""
    text = "HELLO World"
    result = preprocess_text(text, lemmatize=False)
    assert result.islower()


def test_preprocess_text_punctuation_removed():
    """Test punctuation removal."""
    text = "Hello, World! How are you?"
    result = preprocess_text(text, lemmatize=False)
    assert "," not in result
    assert "!" not in result
    assert "?" not in result


def test_tokenize():
    """Test tokenization."""
    text = "hello world test"
    tokens = tokenize(text)
    assert len(tokens) == 3
    assert tokens == ["hello", "world", "test"]


def test_tokenize_empty():
    """Test tokenize with empty string."""
    tokens = tokenize("")
    assert tokens == []


def test_chunk_text():
    """Test text chunking."""
    text = "This is a longer text that should be chunked into multiple parts"
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert len(chunks) > 1
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_chunk_text_short():
    """Test chunking short text."""
    text = "Short text"
    chunks = chunk_text(text, chunk_size=10)
    assert len(chunks) == 1
    assert chunks[0] == text
