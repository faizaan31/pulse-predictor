from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: float = Field(..., ge=-1.0, le=1.0)
    sex: float = Field(..., ge=-1.0, le=1.0)
    bmi: float = Field(..., ge=-1.0, le=1.0)
    bp: float = Field(..., ge=-1.0, le=1.0)
    s1: float = Field(..., ge=-1.0, le=1.0)
    s2: float = Field(..., ge=-1.0, le=1.0)
    s3: float = Field(..., ge=-1.0, le=1.0)
    s4: float = Field(..., ge=-1.0, le=1.0)
    s5: float = Field(..., ge=-1.0, le=1.0)
    s6: float = Field(..., ge=-1.0, le=1.0)


class PredictionResponse(BaseModel):
    prediction: float
    model_version: str
