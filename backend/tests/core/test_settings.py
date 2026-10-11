from pathlib import Path

from clinical_ai.core.settings import BACKEND_DIR, Settings


def test_settings_have_empty_defaults():
    settings = Settings()
    assert settings.openai_api_key.get_secret_value() == ""
    assert settings.openai_model == ""


def test_settings_load_temporary_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=test-secret\nOPENAI_MODEL=test-model\nAPP_ENV=development\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key.get_secret_value() == "test-secret"
    assert settings.openai_model == "test-model"


def test_environment_overrides_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=file-key\nOPENAI_MODEL=file-model\n", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "environment-key")
    monkeypatch.setenv("OPENAI_MODEL", "environment-model")

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key.get_secret_value() == "environment-key"
    assert settings.openai_model == "environment-model"


def test_secret_is_masked_in_representation_and_json():
    settings = Settings(openai_api_key="test-secret", openai_model="test-model")
    assert "test-secret" not in repr(settings)
    assert "test-secret" not in settings.model_dump_json()
    assert settings.openai_api_key.get_secret_value() == "test-secret"


def test_backend_directory_is_independent_of_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    expected = Path(__file__).resolve().parents[2]
    assert BACKEND_DIR == expected
    assert (BACKEND_DIR / "pyproject.toml").is_file()