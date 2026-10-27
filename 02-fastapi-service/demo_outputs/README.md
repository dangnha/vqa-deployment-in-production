Real outputs from the native (no Docker) run on 2026-10-27: uvicorn on port 8701, RTX 3090 (cuda).
The first /predict latency (about 200 ms) includes CUDA warm-up; later requests take about 17 ms.
500 demo: a question repeated 20 times gives 102 text tokens, but ViLT supports at most 40, so the model raises a tensor-size error.
samples/big_image.jpg (7.4 MB) is COCO 39769 upscaled to 4800x3600 with PIL, used for the 413 demo.
