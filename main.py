import asyncio

import uvicorn
from fastapi import FastAPI

from app.api import health_check, channels, rss
from app.db import db

app = FastAPI()

app.include_router(channels.router, prefix="/api/channels", tags=["Channel Management"])
app.include_router(rss.router, prefix="/api/rss", tags=["RSS Reader"])
app.include_router(health_check.router, prefix="/api/checks", tags=["Health Check"])

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await db.init_db()
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
