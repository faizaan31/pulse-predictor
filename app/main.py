import logging

from fastapi import FastAPI

from app.api.routes import build_api_router
from app.core.config import settings
from app.services.prediction_service import PredictionService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

service = PredictionService(model_dir=settings.model_dir)
app = FastAPI(title=settings.app_name)
app.include_router(build_api_router(service))


@app.on_event("startup")
def startup_event() -> None:
    active_model = service.warmup()
    logging.getLogger(__name__).info("API started with model version: %s", active_model)
