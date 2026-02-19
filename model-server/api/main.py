import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from model_server.api.router import router
from model_server.config import settings
from model_server.inference.vlm_engine import vlm_engine

Path("logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level=settings.log_level, colorize=True)
logger.add("logs/model-server.log", rotation="10 MB", retention="7 days", level=settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting model-server...")
    vlm_engine.load()
    yield
    logger.info("Shutting down model-server...")


app = FastAPI(
    title="VLM Model Server",
    description="Qwen2-VL 추론 전용 서버",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

Instrumentator().instrument(app).expose(app)

app.include_router(router)
