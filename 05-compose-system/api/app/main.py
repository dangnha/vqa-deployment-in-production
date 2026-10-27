"""FastAPI app: logging, request timing, SQLite log and model loading at startup."""
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from app import config
from app.models.registry import load_model
from app.routers import vqa
from app.services.request_log import init_db

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the log table, then load the model ONCE before serving
    init_db()
    device = config.get_device()
    logger.info("Loading %s on %s", config.MODEL_NAME, device)
    start = time.perf_counter()
    load_model(device)
    logger.info("Startup finished in %.1fs", time.perf_counter() - start)
    yield


app = FastAPI(title="VQA Service", lifespan=lifespan)
app.include_router(vqa.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log every request: METHOD path -> status in X ms
    start = time.perf_counter()
    response = await call_next(request)
    logger.info("%s %s -> %d in %.0f ms", request.method, request.url.path,
                response.status_code, (time.perf_counter() - start) * 1000)
    return response
