"""
Updated inference service with model caching and batch prediction.
"""

import logging
import os
from pathlib import Path
from typing import Any, Optional

import joblib

from backend.app.ml.preprocessing import preprocess_text
from backend.app.core.exceptions import ModelError
from backend.app.core.config import settings


logger = logging.getLogger(__name__)


class InferenceService:
    """Service for ML model inference."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        vectorizer_path: Optional[str] = None,
    ):
        self.model_path = Path(model_path or settings.ml.model_path or self._default_model_path())
        self.vectorizer_path = Path(
            vectorizer_path or settings.ml.vectorizer_path or self._default_vectorizer_path()
        )

        if not self.model_path.exists():
            raise ModelError(f"Model file not found: {self.model_path}")
        if not self.vectorizer_path.exists():
            raise ModelError(f"Vectorizer file not found: {self.vectorizer_path}")

        try:
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            logger.info(f"Loaded model from {self.model_path}")
        except Exception as e:
            raise ModelError(f"Failed to load model: {e}")

    @staticmethod
    def _project_root() -> Path:
        """Get project root directory."""
        if os.environ.get("VERCEL"):
            return Path("/var/task")
        return Path(__file__).resolve().parents[3]

    def _default_model_path(self) -> Path:
        """Get default model path."""
        project_root = self._project_root()
        preferred = project_root / "models" / "trained" / "model.pkl"
        fallback1 = project_root / "Model" / "model.pkl"
        fallback2 = project_root / "model" / "model.pkl"

        for path in [preferred, fallback1, fallback2]:
            if path.exists():
                return path

        # Return preferred even if doesn't exist (for better error message)
        return preferred

    def _default_vectorizer_path(self) -> Path:
        """Get default vectorizer path."""
        project_root = self._project_root()
        preferred = project_root / "models" / "trained" / "vectorizer.pkl"
        fallback1 = project_root / "Model" / "vectorizer.pkl"
        fallback2 = project_root / "model" / "vectorizer.pkl"

        for path in [preferred, fallback1, fallback2]:
            if path.exists():
                return path

        return preferred

    def predict(self, text: str) -> dict[str, Any]:
        """
        Predict if text is a dark pattern.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with prediction and confidence
        """
        try:
            processed_text = preprocess_text(text)
            features = self.vectorizer.transform([processed_text])
            prediction = int(self.model.predict(features)[0])

            confidence = 1.0
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(features)[0]
                confidence = float(probabilities[prediction])

            return {
                "prediction": prediction,
                "confidence": confidence,
            }
        except Exception as e:
            logger.error(f"Prediction failed: {e}", exc_info=True)
            raise ModelError(f"Prediction failed: {e}")

    def predict_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """
        Predict multiple texts.

        Args:
            texts: List of texts to analyze

        Returns:
            List of predictions
        """
        if not texts:
            return []

        try:
            processed_texts = [preprocess_text(t) for t in texts]
            features = self.vectorizer.transform(processed_texts)
            predictions = self.model.predict(features)

            confidences = [1.0] * len(texts)
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(features)
                confidences = [
                    float(probabilities[i][int(predictions[i])]) for i in range(len(predictions))
                ]

            return [
                {"text": text, "prediction": int(pred), "confidence": conf}
                for text, pred, conf in zip(texts, predictions, confidences)
            ]
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}", exc_info=True)
            raise ModelError(f"Batch prediction failed: {e}")

    def get_model_info(self) -> dict[str, Any]:
        """Get model information."""
        return {
            "model_type": type(self.model).__name__,
            "vectorizer_type": type(self.vectorizer).__name__,
            "model_path": str(self.model_path),
            "vectorizer_path": str(self.vectorizer_path),
        }
