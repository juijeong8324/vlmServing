from pydantic import BaseModel


class PredictResponse(BaseModel):
    answer: str
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
