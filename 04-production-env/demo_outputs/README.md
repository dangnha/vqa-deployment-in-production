# Part 04 demo outputs (real runs, 2026-10-27; RTX 3090, Docker 29.9.2)

- `00_docker_gpu_check.txt` - `docker run --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi` FAILS (no NVIDIA Container Toolkit).
- `01_docker_build_cpu.txt` / `02_docker_build_cuda.txt` - builds of `vqa-api:04-cpu` and `vqa-api:04-cuda`.
- `08_image_sizes.txt` - CPU image 1.7 GB vs CUDA image 9.46 GB on disk.
- `03_gpu_status.txt` - GPU was free before the run (329 MiB used, no processes); our server used 830 MiB.
- `04_native_gpu.txt` - uvicorn on the GPU with `.env` (no Docker): all 7 client cases + timings (~17 ms per answer after a 200 ms first call).
- `05_timeout_504.txt` - `TIMEOUT=0.001` -> 504.
- `06_model_missing_503.txt` - `MODEL_NAME=does-not/exist` -> `/health` 503 and `/predict` 503.
- `07_docker_cpu_fallback.txt` - `vqa-api:04-cpu` with `DEVICE=cuda` in `.env`: warning, falls back to cpu, all 7 cases.
- `09_docker_gpu_run_fails.txt` - `vqa-api:04-cuda` with `--gpus all`: same CDI error. See "GPU support" in ../README.md.

Notes: the 500 is controlled (question repeated 20 times = 102 tokens > ViLT's 40). A real CUDA out-of-memory (503)
cannot be triggered honestly with this small model, so it is not demonstrated. Times inside containers are UTC
(02:11 UTC = 09:11 +07). `FutureWarning` lines from transformers were filtered out.
