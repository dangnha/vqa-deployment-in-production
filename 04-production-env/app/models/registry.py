"""Model registry: load the ViLT model once and share it across requests."""
import logging

from transformers import ViltForQuestionAnswering, ViltProcessor

from app import config

logger = logging.getLogger(__name__)

# Filled once at startup by load_model(): model parts, or an "error" message
registry = {}


def load_model(device):
    # Load processor + model; on failure keep the error so the app still starts
    try:
        processor = ViltProcessor.from_pretrained(config.MODEL_NAME)
        model = ViltForQuestionAnswering.from_pretrained(config.MODEL_NAME)
        model.to(device).eval()
    except Exception as e:
        logger.error("Model loading failed: %s", e)
        registry["error"] = str(e)
        return
    registry["processor"] = processor
    registry["model"] = model
    registry["device"] = device


def get_model():
    # Fail clearly if the model was never loaded
    if not is_loaded():
        raise RuntimeError("Model is not loaded")
    return registry


def is_loaded():
    return "model" in registry
