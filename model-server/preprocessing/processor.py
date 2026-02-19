import io
from PIL import Image

SYSTEM_PROMPT = (
    "You are an expert tutor helping students solve problems. "
    "Analyze the given problem carefully and provide a clear, step-by-step solution. "
    "Show your reasoning process and explain each step. "
    "Use mathematical notation where appropriate."
)


def bytes_to_image(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")


def build_prompt(question: str | None) -> str:
    if question and question.strip():
        return f"{SYSTEM_PROMPT}\n\nStudent's question: {question.strip()}"
    return f"{SYSTEM_PROMPT}\n\nPlease solve the problem shown in the image step by step."
