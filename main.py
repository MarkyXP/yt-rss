import asyncio
import time
import contextlib

import uvicorn
from fastapi import FastAPI, Request

from app.api import health_check, channels, rss
from app.db import db
from app.workflow import periodic_ingest


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: create the background task
    task = asyncio.create_task(periodic_ingest.bg_run_update())
    yield
    # Shutdown logic: cancel the task
    task.cancel()

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def add_timing(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    response.headers["X-Response-Time"] = f"{(end_time - start_time)*1000:.2f}ms"
    return response

app.include_router(channels.router, prefix="/api/channels", tags=["Channel Management"])
app.include_router(rss.router, prefix="/api/rss", tags=["RSS Reader"])
app.include_router(health_check.router, prefix="/api/checks", tags=["Health Check"])

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    await db.init_db()
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
