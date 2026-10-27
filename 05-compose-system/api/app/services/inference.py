"""Run inference in a thread with a timeout, and map errors to HTTP codes."""
import asyncio

import torch
from fastapi import HTTPException

from app import config
from app.models.registry import is_loaded
from app.services.vqa_service import answer_question


async def run_inference(img, question):
    # Run the blocking model call in a thread so the event loop stays free
    try:
        job = asyncio.to_thread(answer_question, img, question)
        return await asyncio.wait_for(job, config.TIMEOUT)
    except asyncio.TimeoutError:
        raise HTTPException(504, f"Inference took longer than {config.TIMEOUT}s")
    except torch.cuda.OutOfMemoryError:
        # Free cached GPU memory so the next request has a chance
        torch.cuda.empty_cache()
        raise HTTPException(503, "GPU out of memory, please retry")
    except Exception as e:
        # Model missing -> 503, any other failure -> 500
        if not is_loaded():
            raise HTTPException(503, str(e))
        raise HTTPException(500, f"Inference failed: {e}")
