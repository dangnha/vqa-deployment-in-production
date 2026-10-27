"""ViLT VQA model: load, preprocess, predict, postprocess."""
import torch
from transformers import ViltForQuestionAnswering, ViltProcessor

MODEL_NAME = "dandelin/vilt-b32-finetuned-vqa"


def load_model(model_name=MODEL_NAME, device="cpu"):
    # Download (or read from cache) the processor and the model weights
    processor = ViltProcessor.from_pretrained(model_name)
    model = ViltForQuestionAnswering.from_pretrained(model_name)
    model.to(device).eval()
    return processor, model


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
