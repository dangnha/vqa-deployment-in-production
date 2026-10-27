# Part 05 - Compose system: API + Streamlit frontend + SQLite log

```bash
cp .env.example .env                 # settings for the api container
docker compose up -d --build         # build both images, start in the background
docker compose ps                    # wait until api is "(healthy)", frontend then starts
# open http://localhost:8702 (Streamlit UI), the API is on http://localhost:8701
python test_system.py                # 10 cases + GET /logs, exit code 1 if any fail
docker compose restart api           # model comes from the hf_cache volume
docker compose logs api              # no download progress bars, just "Loading" + "Startup finished"
docker compose down                  # stops containers, KEEPS the volumes
# docker compose down -v             # would ALSO delete hf_cache and logs
```

## Without Docker

```bash
cd api && uvicorn app.main:app --port 8701              # terminal 1 (log in api/logs/)
API_URL=http://localhost:8701/predict streamlit run frontend/app.py --server.port 8702   # terminal 2, repo root
```

## GPU support

By default the api runs on CPU. Running a GPU container needs the NVIDIA driver on the host plus the
NVIDIA Container Toolkit. On Ubuntu/Debian, first add NVIDIA's apt repository as described in the
[official install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), then:

```bash
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi   # check: prints the GPU table
```

Without the toolkit, GPU containers fail with `could not select device driver` or
`failed to discover GPU vendor from CDI` (part 04 recorded this in `demo_outputs/09_docker_gpu_run_fails.txt`);
the api then still works on CPU.

To use the GPU, edit the api service in `docker-compose.yml`: replace `build: ./api` with the commented
`build: {context: ./api, dockerfile: Dockerfile.cuda}` line and uncomment the `deploy:` /
`resources: ... devices ...` lines below it (the GPU reservation). Keep `DEVICE=cuda` in `.env`,
then run `docker compose up -d --build`.
