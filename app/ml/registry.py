from pathlib import Path
from typing import Optional

from joblib import load

from app.db.postgres import run_query
from app.ml.training import save_model_artifact, train_model


def fetch_active_model_version() -> Optional[str]:
    rows = run_query(
        """
        SELECT model_version
        FROM model_registry
        WHERE is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 1
        """,
        fetch=True,
    )
    if not rows:
        return None
    return str(rows[0][0])


def register_new_model(model_version: str) -> None:
    run_query("UPDATE model_registry SET is_active = FALSE WHERE is_active = TRUE")
    run_query(
        "INSERT INTO model_registry (model_version, is_active) VALUES (%s, TRUE)",
        (model_version,),
    )


def ensure_model_exists(model_dir: Path) -> str:
    current_version = fetch_active_model_version()
    if current_version:
        return current_version

    trained_model = train_model()
    created_version = save_model_artifact(trained_model, model_dir=model_dir)
    register_new_model(created_version)
    return created_version


def load_model_by_version(model_dir: Path, model_version: str):
    artifact_path = model_dir / f"model_{model_version}.joblib"
    if not artifact_path.exists():
        raise FileNotFoundError(f"Model artifact is missing: {artifact_path}")
    return load(artifact_path)
