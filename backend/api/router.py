from typing import Optional

import httpx
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from loguru import logger

from backend.api.schemas import HealthResponse, SolveResponse
from backend.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.model_server_url}/health")
        model_status = "ok" if resp.status_code == 200 else "degraded"
    except Exception:
        model_status = "unreachable"

    return HealthResponse(status="ok", model_server_status=model_status)


@router.post("/api/v1/solve", response_model=SolveResponse)
async def solve(
    image: UploadFile = File(..., description="문제가 담긴 이미지"),
    question: Optional[str] = Form(None, description="추가 질문 (선택)"),
) -> SolveResponse:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    image_bytes = await image.read()
    logger.info(f"Forwarding | file={image.filename!r} question={question!r}")

    files = {"image": (image.filename, image_bytes, image.content_type)}
    data = {"question": question} if question else {}

    try:
        async with httpx.AsyncClient(timeout=settings.model_server_timeout) as client:
            resp = await client.post(
                f"{settings.model_server_url}/predict",
                files=files,
                data=data,
            )
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        logger.error(f"Model server unreachable: {e}")
        raise HTTPException(status_code=503, detail="모델 서버에 연결할 수 없습니다.")

    result = resp.json()
    return SolveResponse(
        answer=result["answer"],
        model=settings.model_server_url,
        latency_ms=result["latency_ms"],
    )
