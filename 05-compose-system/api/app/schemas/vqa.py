"""Pydantic response models for the VQA API."""
from pydantic import BaseModel


class VQAResponse(BaseModel):
    answer: str
    confidence: float
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
