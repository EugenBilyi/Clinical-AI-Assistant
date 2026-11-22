from importlib import import_module
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.testclient import TestClient
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from clinical_ai.main import app

chat_router = import_module("clinical_ai.api.chat.router")


@pytest.fixture
def answer_mock(monkeypatch):
    answer = AsyncMock(return_value="Hello from AI")
    monkeypatch.setattr(chat_router, "answer_message", answer)
    return answer


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize("message", [" Hello ", "Hello", "x" * 10000])
def test_chat_returns_answer(client, answer_mock, message):
    response = client.post("/api/chat/", json={"message": message})

    assert response.status_code == 200
    assert response.json() == {"answer": "Hello from AI"}
    answer_mock.assert_awaited_once_with(message.strip())


@pytest.mark.parametrize("body", [
    {}, {"message": ""}, {"message": " \t\n "},
    {"message": "x" * 10001}, {"message": None},
    {"message": 42}, {"message": []},
])
def test_chat_rejects_invalid_message(client, answer_mock, body):
    response = client.post("/api/chat/", json=body)

    assert response.status_code == 422
    answer_mock.assert_not_awaited()


def test_chat_rejects_malformed_json(client, answer_mock):
    response = client.post(
        "/api/chat/", content="{", headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422
    answer_mock.assert_not_awaited()


@pytest.mark.parametrize("kind,status,detail", [
    ("value", 503, "AI service is unavailable"),
    ("timeout", 504, "AI service timed out"),
    ("auth", 503, "AI service is temporarily unavailable"),
    ("rate", 503, "AI service is temporarily unavailable"),
    ("connection", 502, "Unable to get a response from AI service."),
    ("status", 502, "Unable to get a response from AI service."),
])
def test_chat_sanitizes_errors(client, answer_mock, kind, status, detail):
    request = httpx.Request("POST", "https://api.openai.com/v1/responses")
    private_detail = "private-provider-detail secret-test-key"
    errors = {
        "value": ValueError(private_detail),
        "timeout": APITimeoutError(request=request),
        "auth": AuthenticationError(
            private_detail, response=httpx.Response(401, request=request), body=None,
        ),
        "rate": RateLimitError(
            private_detail, response=httpx.Response(429, request=request), body=None,
        ),
        "connection": APIConnectionError(request=request, message=private_detail),
        "status": APIStatusError(
            private_detail, response=httpx.Response(500, request=request), body=None,
        ),
    }
    answer_mock.side_effect = errors[kind]

    response = client.post("/api/chat/", json={"message": "Hello"})

    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert private_detail not in response.text
    assert "secret-test-key" not in response.text
    answer_mock.assert_awaited_once_with("Hello")


@pytest.mark.parametrize("origin", ["http://localhost:3000", "http://127.0.0.1:3000"])
def test_cors_allows_frontend_preflight(client, answer_mock, origin):
    response = client.options("/api/chat/", headers={
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    })
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    answer_mock.assert_not_awaited()


def test_cors_rejects_unapproved_origin(client, answer_mock):
    response = client.options("/api/chat/", headers={
        "Origin": "https://unapproved.example",
        "Access-Control-Request-Method": "POST",
    })
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
    answer_mock.assert_not_awaited()


def test_chat_response_has_cors_header(client, answer_mock):
    response = client.post(
        "/api/chat/", json={"message": "Hello"},
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"