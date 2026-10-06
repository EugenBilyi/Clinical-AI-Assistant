from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
  openai_api_key: SecretStr = SecretStr("")
  openai_model: str = ""

  model_config = SettingsConfigDict(
    env_file = BACKEND_DIR / ".env",
    env_file_encoding = "utf-8",
    extra = "ignore",
  )