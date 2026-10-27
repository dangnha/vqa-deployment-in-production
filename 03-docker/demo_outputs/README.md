# Part 03 demo outputs (real runs, 2026-10-27, Docker 29.9.2, CPU only)

- `01_docker_build.txt` - first `docker build` (3m47s, pip layer 1.19 GB).
- `02_image_size.txt` - `docker images` / `docker history` for `vqa-api:03` (1.7 GB on disk).
- `03_rebuild_cached.txt` - second build: every layer CACHED.
- `04_first_run.txt` - first `docker run` with an empty `hf_cache/` bind mount: model downloaded, loaded in 65.5 s; cache is 450 MB and owned by the user (thanks to `--user`).
- `05_client_output.txt` - `python client.py` against the container (200, 422, 422, 400, 500).
- `06_second_run_cached.txt` - new container, same bind mount: model loaded in 2.8 s, no download, cache size unchanged.
- `07_curl_errors.txt` - 413 (7.4 MB image) and 400 (text file sent as image/jpeg).

The 500 is controlled: the question is repeated 20 times (102 tokens), longer than ViLT's 40-token limit.
`FutureWarning` lines from transformers were filtered out of the logs.
