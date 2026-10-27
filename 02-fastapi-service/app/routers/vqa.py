"""VQA endpoints: health check and predict."""
import io

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image

from app.models.registry import is_loaded
from app.schemas.vqa import HealthResponse, VQAResponse
from app.services.vqa_service import answer_question

router = APIRouter()
MAX_IMAGE_BYTES = 5 * 1024 * 1024


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok", "model_loaded": is_loaded()}


@router.post("/predict", response_model=VQAResponse)
def predict(image: UploadFile = File(...), question: str = Form(...)):
    # Validate inputs before touching the model
    if not question.strip():
        raise HTTPException(422, "Question must not be empty")
    if image.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(400, f"Unsupported file type: {image.content_type}")
    data = image.file.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image is larger than 5 MB")
    try:
        pil_image = Image.open(io.BytesIO(data))
    except Exception:
        raise HTTPException(400, "File is not a valid image")
    # Run inference: model missing -> 503, any other failure -> 500
    try:
        return answer_question(pil_image, question)
    except Exception as e:
        if not is_loaded():
            raise HTTPException(503, str(e))
        raise HTTPException(500, f"Inference failed: {e}")
