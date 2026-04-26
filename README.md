# PulsePredictor

Real-time ML prediction API built with **FastAPI + PostgreSQL**.

This repository provides a containerized machine learning API for real-time inference.
It demonstrates:
- model caching and version-aware loading at prediction time,
- model update workflows without application redeployment,
- health checks that validate both infrastructure and model availability,
- clean local development and deployment-oriented project organization.

## ⚙️ Tech Stack

- Backend: FastAPI, Uvicorn, Pydantic
- ML: scikit-learn, pandas, NumPy, joblib
- Database: PostgreSQL, psycopg2, Flyway migrations
- Dev setup: Docker, Docker Compose, Makefile
- Tests: pytest, FastAPI TestClient (`httpx`)

## 🔄 How It Works

`Client` -> `FastAPI validation` -> `Versioned model inference` -> `Store prediction in PostgreSQL` -> `JSON response`

## 🧰 Folder Structure

```text
app/
  api/        # FastAPI routes
  core/       # settings + config
  db/         # DB connection/helpers
  ml/         # model training + model registry
  schemas/    # request/response models
  services/   # prediction orchestration logic
migrations/   # Flyway SQL migrations
artifacts/    # trained model files (gitignored)
```

## 🚀 Run The Project

### 1) Prerequisites

- Docker + Docker Compose installed
- `make` installed
- Port `8000` and `5432` available

### 2) Clone and Enter Project

```bash
git clone https://github.com/faizaan31/pulse-predictor.git
cd pulse-predictor
```

### 3) Configure Environment

```bash
make init
```

If needed, edit `.env` (DB user/password, etc.).

### 4) Build and Start Services

```bash
make up
```

### 5) Verify Service Health

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health endpoint: [http://localhost:8000/health](http://localhost:8000/health)

### 6) Test a Prediction

Use this request body in `POST /predict`:

```json
{
  "age": 0.04,
  "sex": -0.02,
  "bmi": 0.03,
  "bp": 0.02,
  "s1": -0.01,
  "s2": -0.02,
  "s3": 0.01,
  "s4": 0.02,
  "s5": 0.03,
  "s6": 0.04
}
```

Expected response: JSON payload containing predicted value and model version.

## 📝 Notes

- `artifacts/` is gitignored and generated during runtime/training.
- `.env` is local-only and should not be committed.
- If docs do not load, check container status with `docker compose ps`.
