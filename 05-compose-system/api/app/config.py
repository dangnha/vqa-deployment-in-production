"""App settings read from environment variables (with safe defaults)."""
import logging
import os

import torch

logger = logging.getLogger(__name__)

# Every setting can be overridden with an env variable (e.g. from .env)
MODEL_NAME = os.getenv("MODEL_NAME", "dandelin/vilt-b32-finetuned-vqa")
DEVICE = os.getenv("DEVICE", "cuda")
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 5 * 1024 * 1024))
TIMEOUT = float(os.getenv("TIMEOUT", 10))


def get_device():
    # Use the GPU only if it was asked for AND is really there
    if DEVICE == "cuda" and torch.cuda.is_available():
        return "cuda"
    logger.warning("DEVICE=%s, CUDA available=%s -> using cpu",
                   DEVICE, torch.cuda.is_available())
    return "cpu"
