"""Run one VQA inference from the command line and time it."""
import sys
import time

import torch
from PIL import Image

from model import load_model, postprocess, predict, preprocess

image_path = sys.argv[1] if len(sys.argv) > 1 else "samples/coco_000000039769.jpg"
question = sys.argv[2] if len(sys.argv) > 2 else "How many cats are there?"
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device     : {device}")

# 1. Load the model once and time it
start = time.perf_counter()
processor, model = load_model(device=device)
load_s = time.perf_counter() - start

# 2. Warm-up run (first call is always slower)
image = Image.open(image_path)
postprocess(model, predict(model, preprocess(processor, image, question, device)))

# 3. Timed run: preprocess + predict + postprocess
start = time.perf_counter()
inputs = preprocess(processor, image, question, device)
result = postprocess(model, predict(model, inputs))
if device == "cuda":
    torch.cuda.synchronize()
infer_ms = (time.perf_counter() - start) * 1000

# 4. Print the results
print(f"Image      : {image_path}")
print(f"Question   : {question}")
print(f"Answer     : {result['answer']}")
print(f"Confidence : {result['confidence']:.4f}")
print(f"Load time  : {load_s:.2f} s")
print(f"Inference  : {infer_ms:.1f} ms")
