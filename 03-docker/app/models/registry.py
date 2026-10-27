"""Model registry: load the ViLT model once and share it across requests."""
from transformers import ViltForQuestionAnswering, ViltProcessor

MODEL_NAME = "dandelin/vilt-b32-finetuned-vqa"

# Filled once at startup by load_model()
registry = {}


def load_model(device):
    # Load processor + model weights, move model to device, eval mode
    processor = ViltProcessor.from_pretrained(MODEL_NAME)
    model = ViltForQuestionAnswering.from_pretrained(MODEL_NAME)
    model.to(device).eval()
    registry["processor"] = processor
    registry["model"] = model
    registry["device"] = device


def get_model():
    # Fail clearly if the model was never loaded
    if not registry:
        raise RuntimeError("Model is not loaded")
    return registry


def is_loaded():
    return bool(registry)
