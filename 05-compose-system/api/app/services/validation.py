"""Input validation for /predict: turn bad uploads into clear HTTP errors."""
import io

from fastapi import HTTPException
from PIL import Image

from app import config

ALLOWED_TYPES = {"image/jpeg", "image/png"}


def read_image(data, content_type):
    # Check type and size first, then make sure Pillow can open the bytes
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {content_type}")
    if len(data) > config.MAX_IMAGE_SIZE:
        limit_mb = config.MAX_IMAGE_SIZE / (1024 * 1024)
        raise HTTPException(413, f"Image is larger than {limit_mb:g} MB")
    try:
        return Image.open(io.BytesIO(data))
    except Exception:
        raise HTTPException(400, "File is not a valid image")
