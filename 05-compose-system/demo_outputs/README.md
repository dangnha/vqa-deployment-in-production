# Part 05 demo outputs (real runs, 2026-10-27, Docker Compose, api on CPU)

- `01_compose_up.txt` - Streamlit frontend image built from scratch (`build --no-cache frontend`, 1m10s, pip 56.4 s), then `docker compose up -d --build` (api layers all CACHED, 7.1 s): waits for api "Healthy", then starts frontend.
- `02_compose_ps.txt` - both services up, api `(healthy)`; images (api 1.7 GB, frontend 834 MB) and the two named volumes.
- `03_test_system.txt` - `python test_system.py`: 10/10 passed (6 answers + 422, 400, 413, 500) and the SQLite rows from `GET /logs`.
- `04_frontend.txt` - Streamlit page on 8702 returns 200 (`/_stcore/health` ok); headless Chromium asked through the UI ("2", 0.9444); inside the frontend container `api` resolves via Compose DNS.
- `05_api_logs_first_start.txt` - first start: model downloaded into the `hf_cache` volume, startup 50.2 s.
- `06_restart_no_download.txt` - `docker compose restart api`: startup 2.3 s, no download; `/logs` rows survive (logs volume); volume holds 450 MB.
- `07_compose_down.txt` - `docker compose down` (volumes kept).
- `streamlit_ui.png` - full-page screenshot (1280 px wide, headless Playwright): uploaded `coco_000000039769.jpg`, "How many cats are there?" -> `Answer: 2`, `Confidence: 0.9444`, raw JSON.

Notes: the empty question `""` is rejected by FastAPI itself ("Field required", 422) before our code, so it is not in
`/logs`; `"   "` would be logged. The 500 is controlled ("cat " * 100 > ViLT's 40 tokens). Times inside containers are
UTC (10:43 UTC = 17:43 +07). The Streamlit "External URL" (server public IP) is redacted in `04_frontend.txt`.
`05_api_logs_first_start.txt` is from the first part 05 run (the model has stayed in the volume since). `FutureWarning`
lines were filtered out. GPU in Compose: see "GPU support" in ../README.md.