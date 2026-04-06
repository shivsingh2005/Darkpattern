import logging
import pickle
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from backend.pipeline.preprocess import preprocess_text


logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parents[1] / "Model"
TYPE_MODEL_PATH = MODEL_DIR / "type_classifier.pkl"
MY_DATA_PATH = MODEL_DIR / "my_data.pkl"
DATASET_PATH = MODEL_DIR / "dark-patterns.csv"


def _load_pickle(path: Path) -> Any:
    try:
        return joblib.load(path)
    except Exception:
        with path.open("rb") as file:
            return pickle.load(file)


def _extract_model_and_vectorizer(obj: Any) -> tuple[Any, Any]:
    if hasattr(obj, "predict"):
        return obj, None

    if isinstance(obj, dict):
        for model_key, vectorizer_key in (
            ("model", "vectorizer"),
            ("classifier", "vectorizer"),
            ("estimator", "vectorizer"),
        ):
            model = obj.get(model_key)
            vectorizer = obj.get(vectorizer_key)
            if hasattr(model, "predict") and hasattr(vectorizer, "transform"):
                return model, vectorizer

    return None, None


def _train_type_model_from_dataset() -> tuple[Any, Any]:
    if not DATASET_PATH.exists():
        raise RuntimeError(f"Dataset not found for category training: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    required_columns = {"Pattern String", "Pattern Category"}
    if not required_columns.issubset(df.columns):
        raise RuntimeError("Dataset is missing required columns for category classifier")

    data = df[["Pattern String", "Pattern Category"]].dropna()
    if data.empty:
        raise RuntimeError("Dataset has no valid rows for category classifier training")

    texts = data["Pattern String"].astype(str).map(preprocess_text)
    labels = data["Pattern Category"].astype(str)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
    features = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    model.fit(features, labels)

    TYPE_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "vectorizer": vectorizer}, TYPE_MODEL_PATH)
    logger.warning("Rebuilt missing/corrupt type classifier and saved to %s", TYPE_MODEL_PATH)
    return model, vectorizer


def _load_or_build_type_model() -> tuple[Any, Any]:
    for candidate in (TYPE_MODEL_PATH, MY_DATA_PATH):
        if not candidate.exists():
            continue
        try:
            loaded = _load_pickle(candidate)
            model, vectorizer = _extract_model_and_vectorizer(loaded)
            if model is not None:
                logger.info("Loaded type classifier from %s", candidate)
                return model, vectorizer
            logger.warning("Ignored unsupported model format in %s", candidate)
        except Exception as exc:
            logger.warning("Failed to load type classifier from %s: %s", candidate, exc)

    return _train_type_model_from_dataset()


try:
    TYPE_CLASSIFIER_MODEL, TYPE_CLASSIFIER_VECTORIZER = _load_or_build_type_model()
except Exception as exc:
    logger.error("Type classifier unavailable: %s", exc)
    TYPE_CLASSIFIER_MODEL, TYPE_CLASSIFIER_VECTORIZER = None, None


def predict_type(text: str) -> dict[str, Any]:
    if TYPE_CLASSIFIER_MODEL is None:
        return {
            "category": "Unknown",
            "confidence": 0.0,
            "all_scores": {},
        }

    try:
        processed_text = preprocess_text(text)
        inference_input = [processed_text]
        if TYPE_CLASSIFIER_VECTORIZER is not None:
            inference_input = TYPE_CLASSIFIER_VECTORIZER.transform(inference_input)

        category = str(TYPE_CLASSIFIER_MODEL.predict(inference_input)[0])

        all_scores: dict[str, float] = {}
        confidence = 1.0

        if hasattr(TYPE_CLASSIFIER_MODEL, "predict_proba") and hasattr(TYPE_CLASSIFIER_MODEL, "classes_"):
            probabilities = TYPE_CLASSIFIER_MODEL.predict_proba(inference_input)[0]
            labels = [str(label) for label in TYPE_CLASSIFIER_MODEL.classes_]
            all_scores = {
                label: float(probabilities[index])
                for index, label in enumerate(labels)
            }
            confidence = float(all_scores.get(category, 1.0))

        return {
            "category": category,
            "confidence": confidence,
            "all_scores": all_scores,
        }
    except Exception as exc:
        raise RuntimeError(f"Type classifier prediction failed: {exc}") from exc
