"""
Updated ML preprocessing module with improved text handling.
"""

import logging
import os
import string
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


logger = logging.getLogger(__name__)

_nltk_data_dir = os.environ.get("NLTK_DATA", "/tmp/nltk_data")
if _nltk_data_dir not in nltk.data.path:
    nltk.data.path.insert(0, _nltk_data_dir)


def _ensure_nltk_resource(resource_path: str, download_name: str) -> None:
    """Ensure NLTK resource is available."""
    try:
        nltk.data.find(resource_path)
    except LookupError:
        try:
            nltk.download(download_name, quiet=True, download_dir=_nltk_data_dir)
        except Exception as e:
            logger.warning(f"Could not download {download_name}: {e}")


_ensure_nltk_resource("corpora/stopwords", "stopwords")
_ensure_nltk_resource("corpora/wordnet", "wordnet")
_ensure_nltk_resource("corpora/omw-1.4", "omw-1.4")


@lru_cache(maxsize=1)
def _stop_words() -> set[str]:
    """Get English stop words."""
    try:
        return set(stopwords.words("english"))
    except Exception as e:
        logger.warning(f"Could not load stopwords: {e}")
        return set()


@lru_cache(maxsize=1)
def _lemmatizer() -> WordNetLemmatizer:
    """Get lemmatizer instance."""
    return WordNetLemmatizer()


def preprocess_text(
    text: str,
    lemmatize: bool = True,
    remove_stopwords: bool = True,
    lowercase: bool = True,
) -> str:
    """
    Preprocess text for ML models.

    Args:
        text: Text to preprocess
        lemmatize: Whether to lemmatize
        remove_stopwords: Whether to remove stopwords
        lowercase: Whether to lowercase

    Returns:
        Preprocessed text
    """
    if not isinstance(text, str):
        text = str(text)

    if not text.strip():
        return ""

    # Lowercase
    if lowercase:
        text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove digits
    text = "".join([char for char in text if not char.isdigit()])

    # Remove stopwords
    if remove_stopwords:
        stop_words = _stop_words()
        text = " ".join([word for word in text.split() if word not in stop_words])

    # Lemmatize
    if lemmatize:
        try:
            lemmatizer = _lemmatizer()
            text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
        except Exception as e:
            logger.warning(f"Lemmatization failed: {e}")

    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Tokenize text into words.

    Args:
        text: Text to tokenize

    Returns:
        List of tokens
    """
    if not text:
        return []
    return text.split()


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    tokens = tokenize(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = " ".join(tokens[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks
