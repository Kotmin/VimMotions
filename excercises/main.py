from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from pydantic import BaseModel

# ---------- Settings ----------
class Settings(BaseModel):
    app_name: str = "fastapi-starter"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    env: str = os.getenv("ENV", "dev")

settings = Settings()

# ---------- Logging ----------
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(settings.app_name)

# ---------- Lifespan (startup/shutdown) ----------
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Startup: init resources (db pool, clients, caches)
    logger.info("Starting %s (env=%s)", settings.app_name, settings.env)
    # Example: await db.connect()
    try:
        yield
    finally:
        # Shutdown: cleanup resources
        logger.info("Stopping %s", settings.app_name)
        # Example: await db.disconnect()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

# ---------- Routes ----------
@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from FastAPI"}

# ---------- Local run ----------
# Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
