from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train_model() -> Pipeline:
    dataset = load_diabetes(as_frame=True)
    features: pd.DataFrame = dataset.data
    target = dataset.target

    model_pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("regressor", Ridge(alpha=1.0)),
        ]
    )
    model_pipeline.fit(features, target)
    return model_pipeline


def save_model_artifact(model_pipeline: Pipeline, model_dir: Path) -> str:
    model_dir.mkdir(parents=True, exist_ok=True)
    version = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    artifact_path = model_dir / f"model_{version}.joblib"
    dump(model_pipeline, artifact_path)
    return version
