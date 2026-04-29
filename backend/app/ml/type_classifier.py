"""
Type classifier for dark pattern categorization.
"""

import logging
import pickle
from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from backend.app.ml.preprocessing import preprocess_text


logger = logging.getLogger(__name__)


class TypeClassifier:
    """Classifier for dark pattern types."""

    def __init__(self, model_path: Optional[Path] = None, vectorizer_path: Optional[Path] = None):
        self.model_path = model_path or self._default_model_path()
        self.vectorizer_path = vectorizer_path or self._default_vectorizer_path()

        self.model = None
        self.vectorizer = None
        self._load_models()

    @staticmethod
    def _default_model_path() -> Path:
        """Get default model path."""
        project_root = Path(__file__).resolve().parents[3]
        for path in [
            project_root / "models" / "trained" / "type_classifier.pkl",
            project_root / "Model" / "type_classifier.pkl",
        ]:
            if path.exists():
                return path
        return project_root / "Model" / "type_classifier.pkl"

    @staticmethod
    def _default_vectorizer_path() -> Path:
        """Get default vectorizer path (not used for type classifier)."""
        return Path()

    def _load_models(self) -> None:
        """Load model and vectorizer."""
        try:
            if self.model_path.exists():
                loaded = joblib.load(self.model_path)
                if isinstance(loaded, dict):
                    self.model = loaded.get("model")
                    self.vectorizer = loaded.get("vectorizer")
                else:
                    self.model = loaded
        except Exception as e:
            logger.warning(f"Could not load type classifier: {e}")

    def predict(self, text: str) -> dict[str, Any]:
        """
        Predict pattern type.

        Args:
            text: Text to classify

        Returns:
            Dictionary with category and confidence
        """
        if not self.model or not self.vectorizer:
            logger.warning("Type classifier not available, returning default")
            return {"category": "Unknown", "confidence": 0.0}

        try:
            processed = preprocess_text(text)
            features = self.vectorizer.transform([processed])
            prediction = self.model.predict(features)[0]
            confidence = 1.0

            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(features)[0]
                confidence = float(max(probabilities))

            return {"category": str(prediction), "confidence": confidence}
        except Exception as e:
            logger.error(f"Type prediction failed: {e}")
            return {"category": "Unknown", "confidence": 0.0}


# Global instance
_type_classifier = None


def get_type_classifier() -> TypeClassifier:
    """Get type classifier instance."""
    global _type_classifier
    if _type_classifier is None:
        _type_classifier = TypeClassifier()
    return _type_classifier


def predict_type(text: str) -> dict[str, Any]:
    """
    Predict dark pattern type.

    Args:
        text: Text to classify

    Returns:
        Dictionary with type and confidence
    """
    classifier = get_type_classifier()
    return classifier.predict(text)
