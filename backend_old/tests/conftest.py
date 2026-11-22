import pytest

from clinical_ai.core.settings import Settings
from clinical_ai.integrations import openai_client


@pytest.fixture(autouse=True)
def isolate_configuration_and_provider(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.setitem(Settings.model_config, "env_file", None)

    def reject_real_client(*args, **kwargs):
        raise AssertionError("Tests must mock the OpenAI client")

    monkeypatch.setattr(openai_client, "AsyncOpenAI", reject_real_client)