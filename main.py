from fastapi import FastAPI

from app.api import health, updater, user_settings

app = FastAPI()

app.include_router(user_settings.router, prefix="/api/user_settings", tags=["Settings"])
app.include_router(updater.router, prefix="/api/update", tags=["Updater"])
app.include_router(health.router, prefix="/api/health", tags=["HealthCheck"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000)
