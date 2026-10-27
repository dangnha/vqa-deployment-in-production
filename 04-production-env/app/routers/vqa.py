"""VQA endpoints: health check and async predict."""
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.models.registry import is_loaded, registry
from app.schemas.vqa import HealthResponse, VQAResponse
from app.services.inference import run_inference
from app.services.validation import read_image

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
def health():
    # 503 tells Docker / a load balancer: do not send traffic here
    if not is_loaded():
        error = {"status": "error", "model_loaded": False, "error": registry.get("error")}
        return JSONResponse(status_code=503, content=error)
    return {"status": "ok", "model_loaded": True, "device": registry["device"]}


@router.post("/predict", response_model=VQAResponse)
async def predict(image: UploadFile = File(...), question: str = Form(...)):
    # Validate inputs before touching the model
    if not question.strip():
        raise HTTPException(422, "Question must not be empty")
    img = read_image(await image.read(), image.content_type)
    # Run the model (timeout + error mapping live in the service)
    result = await run_inference(img, question)
    logger.info("Q=%r A=%r in %s ms", question, result["answer"], result["latency_ms"])
    return result
