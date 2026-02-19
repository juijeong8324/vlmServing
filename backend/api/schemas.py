from pydantic import BaseModel


class SolveResponse(BaseModel):
    answer: str
    model: str
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    model_server_status: str
