import asyncio
from unittest.mock import AsyncMock

import pytest

from clinical_ai.core.settings import Settings
from clinical_ai.services import chat


@pytest.fixture
def service_dependencies(monkeypatch):
    settings = Settings(openai_api_key="test-key", openai_model="test-model")
    generate = AsyncMock(return_value="Hello from AI")
    monkeypatch.setattr(chat, "Settings", lambda: settings)
    monkeypatch.setattr(chat, "generate_answer", generate)
    return settings, generate


def test_service_passes_message_and_settings(service_dependencies):
    settings, generate = service_dependencies

    answer = asyncio.run(chat.answer_message("Hello"))

    assert answer == "Hello from AI"
    generate.assert_awaited_once_with("Hello", settings)


@pytest.mark.parametrize("key,model,error", [
    ("", "test-model", "OpenAI API key is not configured."),
    ("   ", "test-model", "OpenAI API key is not configured."),
    ("test-key", "", "OpenAI model is not configured."),
    ("test-key", "   ", "OpenAI model is not configured."),
])
def test_service_rejects_missing_configuration(
    service_dependencies, monkeypatch, key, model, error,
):
    _, generate = service_dependencies
    settings = Settings(openai_api_key=key, openai_model=model)
    monkeypatch.setattr(chat, "Settings", lambda: settings)

    with pytest.raises(ValueError, match=error.replace(".", r"\.")):
        asyncio.run(chat.answer_message("Hello"))

    generate.assert_not_awaited()


@pytest.mark.parametrize("answer", ["", " \t\n "])
def test_service_rejects_empty_provider_answer(service_dependencies, answer):
    _, generate = service_dependencies
    generate.return_value = answer

    with pytest.raises(ValueError, match="OpenAI returned an empty answer"):
        asyncio.run(chat.answer_message("Hello"))


def test_service_propagates_provider_error(service_dependencies):
    _, generate = service_dependencies
    error = RuntimeError("provider failed")
    generate.side_effect = error

    with pytest.raises(RuntimeError) as raised:
        asyncio.run(chat.answer_message("Hello"))

    assert raised.value is error