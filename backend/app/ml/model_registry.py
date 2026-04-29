"""
Model registry and versioning system.
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)


class ModelStatus(str, Enum):
    """Model status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    FAILED = "failed"


@dataclass
class ModelMetadata:
    """Model metadata."""

    version: str
    model_type: str
    created_at: str
    updated_at: str
    status: ModelStatus = ModelStatus.ACTIVE
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    training_samples: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "ModelMetadata":
        """Create from dictionary."""
        data["status"] = ModelStatus(data.get("status", "active"))
        return cls(**data)


class ModelRegistry:
    """Model registry for managing multiple model versions."""

    def __init__(self, registry_dir: Path = Path("./models/registry")):
        self.registry_dir = registry_dir
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.registry_dir / "metadata.json"

    def register_model(
        self,
        version: str,
        model_path: Path,
        model_type: str = "logistic_regression",
        metadata: Optional[dict] = None,
    ) -> ModelMetadata:
        """
        Register a new model version.

        Args:
            version: Model version string
            model_path: Path to model file
            model_type: Type of model
            metadata: Additional metadata

        Returns:
            ModelMetadata instance
        """
        now = datetime.utcnow().isoformat()
        model_metadata = ModelMetadata(
            version=version,
            model_type=model_type,
            created_at=now,
            updated_at=now,
            **metadata or {},
        )

        self._save_metadata(model_metadata)
        logger.info(f"Registered model version {version}")
        return model_metadata

    def get_active_model(self) -> Optional[ModelMetadata]:
        """Get the currently active model."""
        metadata_list = self._load_all_metadata()
        active_models = [m for m in metadata_list if m.status == ModelStatus.ACTIVE]
        if not active_models:
            return None
        return sorted(active_models, key=lambda m: m.created_at, reverse=True)[0]

    def get_model(self, version: str) -> Optional[ModelMetadata]:
        """Get model by version."""
        metadata_list = self._load_all_metadata()
        for m in metadata_list:
            if m.version == version:
                return m
        return None

    def update_model_status(self, version: str, status: ModelStatus) -> bool:
        """Update model status."""
        metadata_list = self._load_all_metadata()
        for m in metadata_list:
            if m.version == version:
                m.status = status
                m.updated_at = datetime.utcnow().isoformat()
                self._save_all_metadata(metadata_list)
                logger.info(f"Updated model {version} status to {status.value}")
                return True
        return False

    def list_models(self) -> list[ModelMetadata]:
        """List all registered models."""
        return self._load_all_metadata()

    def _save_metadata(self, metadata: ModelMetadata) -> None:
        """Save model metadata."""
        metadata_list = self._load_all_metadata()
        # Remove existing version if present
        metadata_list = [m for m in metadata_list if m.version != metadata.version]
        metadata_list.append(metadata)
        self._save_all_metadata(metadata_list)

    def _load_all_metadata(self) -> list[ModelMetadata]:
        """Load all model metadata."""
        if not self.metadata_file.exists():
            return []
        try:
            with open(self.metadata_file) as f:
                data = json.load(f)
            return [ModelMetadata.from_dict(m) for m in data]
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            return []

    def _save_all_metadata(self, metadata_list: list[ModelMetadata]) -> None:
        """Save all model metadata."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump([m.to_dict() for m in metadata_list], f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")


# Global registry instance
model_registry = ModelRegistry()
