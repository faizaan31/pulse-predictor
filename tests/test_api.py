import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app  # noqa: E402


def test_health_endpoint_returns_status() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "ok"
    assert payload["model"] in {"ok", "not-initialized"}


def test_predict_endpoint_returns_prediction() -> None:
    client = TestClient(app)
    response = client.post(
        "/predict",
        json={
            "age": 0.04,
            "sex": -0.02,
            "bmi": 0.03,
            "bp": 0.02,
            "s1": -0.01,
            "s2": -0.02,
            "s3": 0.01,
            "s4": 0.02,
            "s5": 0.03,
            "s6": 0.04,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "prediction" in payload
    assert isinstance(payload["prediction"], float)
    assert "model_version" in payload
