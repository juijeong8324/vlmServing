from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from loguru import logger

from model_server.api.schemas import HealthResponse, PredictResponse
from model_server.inference.vlm_engine import vlm_engine
from model_server.preprocessing.processor import build_prompt, bytes_to_image

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=vlm_engine._loaded)


@router.post("/predict", response_model=PredictResponse)
async def predict(
    image: UploadFile = File(...),
    question: Optional[str] = Form(None),
) -> PredictResponse:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 허용됩니다.")

    image_bytes = await image.read()
    pil_image = bytes_to_image(image_bytes)
    prompt = build_prompt(question)

    logger.info(f"Predict | file={image.filename!r} question={question!r}")

    try:
        answer, latency_ms = vlm_engine.predict(pil_image, prompt)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        raise HTTPException(status_code=500, detail="추론 중 오류 발생")

    logger.info(f"Done | latency={latency_ms:.1f}ms")
    return PredictResponse(answer=answer, latency_ms=latency_ms)
