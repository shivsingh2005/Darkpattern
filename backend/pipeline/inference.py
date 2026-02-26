import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib

from pipeline.preprocess import preprocess_text


class InferenceService:
    def __init__(self, model_path: Optional[str] = None, vectorizer_path: Optional[str] = None):
        self.model_path = Path(model_path).resolve() if model_path else self._default_model_path()
        self.vectorizer_path = (
            Path(vectorizer_path).resolve() if vectorizer_path else self._default_vectorizer_path()
        )

        if not self.model_path.exists():
            raise RuntimeError(f"Model file not found: {self.model_path}")
        if not self.vectorizer_path.exists():
            raise RuntimeError(f"Vectorizer file not found: {self.vectorizer_path}")

        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    @staticmethod
    def _project_root() -> Path:
        if os.environ.get("VERCEL"):
            return Path("/var/task")
        return Path(__file__).resolve().parents[2]

    def _default_model_path(self) -> Path:
        project_root = self._project_root()
        preferred = project_root / "model" / "model.pkl"
        fallback = project_root / "Model" / "model.pkl"
        return preferred if preferred.exists() else fallback

    def _default_vectorizer_path(self) -> Path:
        project_root = self._project_root()
        preferred = project_root / "model" / "vectorizer.pkl"
        fallback = project_root / "Model" / "vectorizer.pkl"
        return preferred if preferred.exists() else fallback

    def predict(self, text: str) -> dict:
        processed_text = preprocess_text(text)
        features = self.vectorizer.transform([processed_text])

        prediction = int(self.model.predict(features)[0])

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(features)[0]
            confidence = float(probabilities[prediction])
        else:
            confidence = 1.0

        return {
            "prediction": prediction,
            "confidence": confidence,
        }

    def predict_chunks(self, chunks: List[str]) -> List[Dict[str, Any]]:
        if not chunks:
            return []

        indexed_processed = []
        for index, chunk in enumerate(chunks):
            processed = preprocess_text(chunk)
            if processed.strip():
                indexed_processed.append((index, chunk, processed))

        if not indexed_processed:
            return []

        processed_chunks = [item[2] for item in indexed_processed]
        features = self.vectorizer.transform(processed_chunks)
        predictions = self.model.predict(features)

        probabilities = None
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(features)

        results: List[Dict[str, Any]] = []
        for prediction_index, (index, chunk, _) in enumerate(indexed_processed):
            prediction = int(predictions[prediction_index])
            confidence = (
                float(probabilities[prediction_index][prediction])
                if probabilities is not None
                else 1.0
            )
            results.append(
                {
                    "text": chunk,
                    "prediction": prediction,
                    "confidence": confidence,
                }
            )

        return results
