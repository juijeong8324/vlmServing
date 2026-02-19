import io
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image


def _png_bytes() -> bytes:
    img = Image.new("RGB", (64, 64), color=(128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── model-server ──────────────────────────────────────────────────────────────

@pytest.fixture
def model_client():
    with patch("model_server.inference.vlm_engine.VLMEngine.load"):
        from model_server.api.main import app
        with TestClient(app) as c:
            yield c


def test_model_server_health(model_client: TestClient):
    resp = model_client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_model_server_predict(model_client: TestClient):
    mock_answer = "Step 1: x = -1"
    with patch(
        "model_server.inference.vlm_engine.vlm_engine.predict",
        return_value=(mock_answer, 500.0),
    ):
        resp = model_client.post(
            "/predict",
            files={"image": ("test.png", _png_bytes(), "image/png")},
            data={"question": "풀어줘"},
        )
    assert resp.status_code == 200
    assert resp.json()["answer"] == mock_answer


def test_model_server_rejects_non_image(model_client: TestClient):
    resp = model_client.post(
        "/predict",
        files={"image": ("file.txt", b"hello", "text/plain")},
    )
    assert resp.status_code == 400


# ── backend ───────────────────────────────────────────────────────────────────

@pytest.fixture
def backend_client():
    from backend.api.main import app
    with TestClient(app) as c:
        yield c


def test_backend_index_returns_html(backend_client: TestClient):
    resp = backend_client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_backend_solve_forwards_to_model_server(backend_client: TestClient):
    mock_response = {"answer": "Step 1: x = -1", "latency_ms": 800.0}

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_resp = AsyncMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_resp.raise_for_status = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        resp = backend_client.post(
            "/api/v1/solve",
            files={"image": ("test.png", _png_bytes(), "image/png")},
            data={"question": "풀어줘"},
        )
    assert resp.status_code == 200
    assert resp.json()["answer"] == mock_response["answer"]
