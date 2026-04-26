from fastapi import APIRouter, HTTPException

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService


def build_api_router(prediction_service: PredictionService) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health_check() -> dict[str, str]:
        return prediction_service.health()

    @router.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest) -> PredictionResponse:
        try:
            prediction_value, model_version = prediction_service.predict(payload)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
        return PredictionResponse(prediction=prediction_value, model_version=model_version)

    return router
