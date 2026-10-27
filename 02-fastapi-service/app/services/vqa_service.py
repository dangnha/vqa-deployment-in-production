"""VQA inference logic: preprocess, predict, postprocess (no FastAPI here)."""
import time

import torch

from app.models.registry import get_model


def preprocess(processor, image, question, device):
    # Turn image + question into tensors (no truncation on purpose)
    inputs = processor(image.convert("RGB"), question, return_tensors="pt")
    return {k: v.to(device) for k, v in inputs.items()}


def predict(model, inputs):
    # Forward pass without computing gradients
    with torch.no_grad():
        return model(**inputs).logits


def postprocess(model, logits):
    # Softmax -> best class -> human-readable label
    probs = torch.softmax(logits, dim=-1)[0]
    idx = int(probs.argmax())
    return {
        "answer": model.config.id2label[idx],
        "confidence": round(float(probs[idx]), 4),
    }


def answer_question(image, question):
    # Get the shared model, run the 3 steps and measure latency
    m = get_model()
    start = time.perf_counter()
    inputs = preprocess(m["processor"], image, question, m["device"])
    result = postprocess(m["model"], predict(m["model"], inputs))
    result["latency_ms"] = round((time.perf_counter() - start) * 1000, 1)
    return result
