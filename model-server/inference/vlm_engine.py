import time

import torch
from loguru import logger
from PIL import Image
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

from model_server.config import settings

_DTYPE_MAP = {
    "float16": torch.float16,
    "bfloat16": torch.bfloat16,
    "float32": torch.float32,
}

class VLMEngine:
    def __init__(self) -> None:
        self.model: Qwen2_5_VLForConditionalGeneration | None = None
        self.processor: AutoProcessor | None = None
        self._loaded = False

    def load(self) -> None:
        logger.info(f"Loading model: {settings.model_name}")
        dtype = _DTYPE_MAP[settings.model_dtype]

        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            settings.model_name,
            torch_dtype=dtype,
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(settings.model_name)
        self._loaded = True
        logger.info("Model loaded successfully")

    def predict(self, image: Image.Image, prompt: str) -> tuple[str, float]:
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            return_tensors="pt",
        ).to(self.model.device)

        start = time.perf_counter()
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=settings.max_new_tokens,
                temperature=settings.temperature,
                do_sample=settings.temperature > 0,
            )
        latency_ms = (time.perf_counter() - start) * 1000

        generated_ids = [
            out[len(inp):]
            for inp, out in zip(inputs.input_ids, output_ids)
        ]
        answer = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )[0]

        return answer, latency_ms


vlm_engine = VLMEngine()
