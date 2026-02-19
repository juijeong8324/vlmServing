import io

import pytest
from PIL import Image

from model_server.preprocessing.processor import SYSTEM_PROMPT, build_prompt, bytes_to_image


def _make_image_bytes(width: int = 10, height: int = 10) -> bytes:
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_bytes_to_image_returns_pil_image():
    result = bytes_to_image(_make_image_bytes())
    assert isinstance(result, Image.Image)
    assert result.mode == "RGB"


def test_bytes_to_image_preserves_size():
    result = bytes_to_image(_make_image_bytes(100, 200))
    assert result.size == (100, 200)


def test_build_prompt_with_question():
    prompt = build_prompt("x^2 + 2x + 1 = 0을 풀어줘")
    assert "x^2 + 2x + 1 = 0을 풀어줘" in prompt
    assert SYSTEM_PROMPT in prompt


def test_build_prompt_without_question():
    prompt = build_prompt(None)
    assert "step by step" in prompt
    assert SYSTEM_PROMPT in prompt


def test_build_prompt_empty_string_treated_as_none():
    prompt = build_prompt("")
    assert "step by step" in prompt
