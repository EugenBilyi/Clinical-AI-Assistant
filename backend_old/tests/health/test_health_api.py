from fastapi.testclient import TestClient

from clinical_ai.main import app


def test_health_returns_ok_without_openai_configuration():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}