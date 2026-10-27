# Part 04 - Production environment

The part 03 VQA service, configured by env variables, with logging, timeouts and clear errors.

| Variable | Default | Meaning |
|---|---|---|
| `MODEL_NAME` | `dandelin/vilt-b32-finetuned-vqa` | Hugging Face model id |
| `DEVICE` | `cuda` | `cuda` or `cpu` (falls back to cpu if no GPU) |
| `MAX_IMAGE_SIZE` | `5242880` (5 MB) | Max upload size in bytes -> 413 |
| `TIMEOUT` | `10` | Max inference time in seconds -> 504 |

```bash
cp .env.example .env              # then edit .env (it is git-ignored)
docker build -t vqa-api:04-cpu .
docker build -f Dockerfile.cuda -t vqa-api:04-cuda .
# run on CPU, or on GPU (needs the NVIDIA Container Toolkit, see "GPU support")
mkdir -p hf_cache
docker run --rm --env-file .env -p 8701:8000 --user "$(id -u):$(id -g)" -v "$(pwd)/hf_cache:/hf_cache" vqa-api:04-cpu
docker run --rm --gpus all --env-file .env -p 8701:8000 --user "$(id -u):$(id -g)" -v "$(pwd)/hf_cache:/hf_cache" vqa-api:04-cuda
```

Without Docker: `set -a; source .env; set +a; HF_HOME=./hf_cache uvicorn app.main:app --port 8701`

Test: `python client.py` (case (g) sends a JPEG padded in memory to just over 6 MB -> 413). Docs: http://localhost:8701/docs

## See the errors

- `TIMEOUT=0.001` in `.env` -> every `/predict` returns **504**.
- `MODEL_NAME=does-not/exist` -> the app still starts, `/health` returns **503** with the load error.
- Every request is logged as `METHOD path -> status in X ms`.

## GPU support

Running a GPU container needs the NVIDIA driver on the host plus the NVIDIA Container Toolkit.
On Ubuntu/Debian, first add NVIDIA's apt repository as described in the
[official install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), then:

```bash
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi   # check: prints the GPU table
```

Without the toolkit, `docker run --gpus all` fails with `could not select device driver` or
`failed to discover GPU vendor from CDI` (see `demo_outputs/09_docker_gpu_run_fails.txt`);
the CPU image (and the app with `DEVICE=cpu` or no GPU) still works.

With the toolkit installed: build `Dockerfile.cuda` (`docker build -f Dockerfile.cuda -t vqa-api:04-cuda .`),
set `DEVICE=cuda` in `.env`, and run the `vqa-api:04-cuda` command above with `--gpus all`.
