"""VQA endpoints: health check, async predict (logged to SQLite) and logs."""
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from app.models.registry import is_loaded, registry
from app.schemas.vqa import HealthResponse, VQAResponse
from app.services.inference import run_inference
from app.services.request_log import log_request, recent
from app.services.validation import read_image

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    # 503 tells Docker / a load balancer: do not send traffic here
    if not is_loaded():
        error = {"status": "error", "model_loaded": False, "error": registry.get("error")}
        return JSONResponse(status_code=503, content=error)
    return {"status": "ok", "model_loaded": True, "device": registry["device"]}


@router.post("/predict", response_model=VQAResponse)
async def predict(image: UploadFile = File(...), question: str = Form(...)):
    # Validate, run the model, and log the call (answer None on errors)
    try:
        if not question.strip():
            raise HTTPException(422, "Question must not be empty")
        img = read_image(await image.read(), image.content_type)
        result = await run_inference(img, question)
    except HTTPException as e:
        log_request(question, None, None, None, e.status_code)
        raise
    log_request(question, result["answer"], result["confidence"],
                result["latency_ms"], 200)
    return result


@router.get("/logs")
def logs():
    return recent()  # last 10 rows from the SQLite log, newest first
