from openai import AsyncOpenAI

from clinical_ai.core.settings import Settings


async def generate_answer (message: str, settings: Settings) -> str:
  async with AsyncOpenAI(
    api_key = settings.openai_api_key.get_secret_value(),
    timeout = 10.0,
    max_retries = 0,
  ) as client:
    response = await client.responses.create(
      model = settings.openai_model,
      input = message,
      store = False,
    )

  return response.output_text