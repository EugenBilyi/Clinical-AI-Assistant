from clinical_ai.core.settings import Settings
from clinical_ai.integrations.openai_client import generate_answer


async def answer_message(message: str) -> str:
  settings = Settings()

  if not settings.openai_api_key.get_secret_value().strip():
    raise ValueError("OpenAI API key is not configured.")
  if not settings.openai_model.strip():
    raise ValueError("OpenAI model is not configured.")

  answer = await generate_answer(message, settings)

  if not answer.strip():
    raise ValueError("OpenAI returned an empty answer.")

  return answer