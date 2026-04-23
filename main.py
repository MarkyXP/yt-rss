import asyncio
import contextlib
import os
import time

import uvicorn
from fastapi import FastAPI, Request
from loguru import logger

from app.adapters.out_rss_feed import api
from app.api import health_check, subscriptions, user_management
from app.core.config import CONFIG
from app.db import db
from app.workflow import periodic_index


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    ## Startup logic
    # Create logs output
    os.makedirs(".logs", exist_ok=True)
    logger.add(".logs/app.log", enqueue=True, rotation="1 day", retention="14 days")
    # Create the background task
    task_run_update_bg = asyncio.create_task(periodic_index.bg_run_update())
    yield
    # Shutdown logic: cancel the task
    task_run_update_bg.cancel()
    await logger.complete()

app = FastAPI(lifespan=lifespan, version=CONFIG.APP_VERSION)


@app.middleware("http")
async def add_timing(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    response.headers["X-Response-Time"] = f"{(end_time - start_time)*1000:.2f}ms"
    return response

app.include_router(subscriptions.router, prefix="/api/channels", tags=["Channel Management"])
app.include_router(api.router, prefix="/api/v0.1/rss", tags=["RSS Reader"])
if CONFIG.ADMIN_PASSWORD:
    app.include_router(user_management.router, prefix="/user", tags=["User Management"])
app.include_router(health_check.router, prefix="/api/checks", tags=["Health Check"])

async def main():
    config = uvicorn.Config(
        app = "main:app",
        host=CONFIG.YTRSS_HOST,
        port=CONFIG.YTRSS_PORT,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await db.init_db()
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
