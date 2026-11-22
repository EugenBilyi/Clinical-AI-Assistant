import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from clinical_ai.core.settings import Settings
from clinical_ai.integrations import openai_client
from clinical_ai.main import app
from clinical_ai.services import chat


@pytest.fixture
def provider(monkeypatch):
    create = AsyncMock(return_value=SimpleNamespace(output_text="Hello from AI"))
    client = SimpleNamespace(responses=SimpleNamespace(create=create))
    context = MagicMock()
    context.__aenter__ = AsyncMock(return_value=client)
    context.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock(return_value=context)
    monkeypatch.setattr(openai_client, "AsyncOpenAI", factory)
    settings = Settings(openai_api_key="test-key", openai_model="test-model")
    return settings, factory, context, create


def test_client_calls_responses_api_and_closes(provider):
    settings, factory, context, create = provider

    answer = asyncio.run(openai_client.generate_answer("Hello", settings))

    assert answer == "Hello from AI"
    factory.assert_called_once_with(api_key="test-key", timeout=10.0, max_retries=0)
    create.assert_awaited_once_with(model="test-model", input="Hello", store=False)
    context.__aenter__.assert_awaited_once_with()
    context.__aexit__.assert_awaited_once_with(None, None, None)


def test_client_closes_and_propagates_request_error(provider):
    settings, _, context, create = provider
    error = RuntimeError("provider failed")
    create.side_effect = error

    with pytest.raises(RuntimeError) as raised:
        asyncio.run(openai_client.generate_answer("Hello", settings))

    assert raised.value is error
    context.__aexit__.assert_awaited_once()
    exit_type, exit_error, _ = context.__aexit__.await_args.args
    assert exit_type is RuntimeError
    assert exit_error is error


def test_http_chat_runs_service_and_mocked_sdk(provider, monkeypatch):
    settings, _, _, create = provider
    monkeypatch.setattr(chat, "Settings", lambda: settings)

    with TestClient(app) as client:
        response = client.post("/api/chat/", json={"message": " Hello "})

    assert response.status_code == 200
    assert response.json() == {"answer": "Hello from AI"}
    create.assert_awaited_once_with(model="test-model", input="Hello", store=False)