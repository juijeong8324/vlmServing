import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from backend.api.router import router
from backend.config import settings

Path("logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level=settings.log_level, colorize=True)
logger.add("logs/backend.log", rotation="10 MB", retention="7 days", level=settings.log_level)

app = FastAPI(
    title="VLM Problem Solver — Backend",
    description="API 게이트웨이",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

Instrumentator().instrument(app).expose(app)

app.include_router(router)
