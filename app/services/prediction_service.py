from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from app.db.postgres import as_json, run_query
from app.ml.registry import ensure_model_exists, fetch_active_model_version, load_model_by_version
from app.schemas.prediction import PredictionRequest


@dataclass
class ModelCache:
    version: str | None = None
    pipeline: Any = None


class PredictionService:
    def __init__(self, model_dir: Path) -> None:
        self.model_dir = model_dir
        self.cache = ModelCache()

    def warmup(self) -> str:
        active_version = ensure_model_exists(self.model_dir)
        self._refresh_model_if_needed(active_version)
        return active_version

    def health(self) -> dict[str, str]:
        db_ok = bool(run_query("SELECT 1", fetch=True))
        active_version = fetch_active_model_version()
        model_status = "ok" if active_version else "not-initialized"
        return {
            "service": "ok",
            "database": "ok" if db_ok else "unavailable",
            "model": model_status,
        }

    def predict(self, request_data: PredictionRequest) -> tuple[float, str]:
        active_version = ensure_model_exists(self.model_dir)
        self._refresh_model_if_needed(active_version)

        features = pd.DataFrame([request_data.dict()])
        prediction_value = float(self.cache.pipeline.predict(features)[0])

        run_query(
            "INSERT INTO predictions (model_version, features_payload, prediction) VALUES (%s, %s, %s)",
            (active_version, as_json(request_data.dict()), prediction_value),
        )
        return prediction_value, active_version

    def _refresh_model_if_needed(self, required_version: str) -> None:
        if self.cache.version == required_version and self.cache.pipeline is not None:
            return
        self.cache.pipeline = load_model_by_version(self.model_dir, required_version)
        self.cache.version = required_version
