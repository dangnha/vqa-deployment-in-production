# Part 01 - Inference pipeline

Loads ViLT (`dandelin/vilt-b32-finetuned-vqa`) once and answers one question about one image. Inference is split
into three steps: preprocess (image + question to tensors), predict (forward pass without gradients) and
postprocess (softmax to answer + confidence). After one warm-up call, `run.py` times the model load and a full
preprocess + predict + postprocess call. It uses the GPU if one is available, otherwise the CPU.

- `model.py`: `load_model`, `preprocess`, `predict`, `postprocess`
- `run.py`: command-line entry point, `python run.py [image] [question]`
- `requirements.txt`: torch, transformers, pillow
- `samples/`: three COCO images (attribution and licenses in `samples/SOURCES.md`)
- `demo_outputs/`: terminal output recorded from real runs

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py samples/coco_000000039769.jpg "How many cats are there?"
```

Without arguments, `run.py` uses this same image and question. It prints the device, image, question, answer,
confidence, load time and inference time. To force the CPU on a GPU machine: `CUDA_VISIBLE_DEVICES="" python run.py`.

Results in `demo_outputs/` (RTX 3090 for GPU):

| Question | Answer | Confidence | GPU | CPU |
|----------|--------|------------|-----|-----|
| How many cats are there? | 2 | 0.9444 | 17.4 ms | 110.9 ms |
| What room is this? (`000000000139`) | dining room | 0.5902 | 18.8 ms | 120.8 ms |
| What is on the bed? | pillows | 0.3828 | 16.5 ms | 93.1 ms |

Load time is about 2.4-2.9 s with the model cached (CPU and GPU). The first run (GPU) took 52.26 s to load
because it downloaded the weights (about 450 MB on disk).
