"""FastAPI app: load the model once at startup and mount the VQA router."""
import time
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI

from app.models.registry import load_model
from app.routers import vqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pick the device and load the model ONCE before serving requests
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    start = time.perf_counter()
    load_model(device)
    print(f"Model loaded in {time.perf_counter() - start:.1f}s")
    yield


app = FastAPI(title="VQA Service", lifespan=lifespan)
app.include_router(vqa.router)
