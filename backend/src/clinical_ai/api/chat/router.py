from fastapi import APIRouter, HTTPException
from openai import (
  APIConnectionError,
  APIStatusError,
  APITimeoutError,
  AuthenticationError,
  RateLimitError,
)

from clinical_ai.api.chat import schemas
from clinical_ai.services.chat import answer_message

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=schemas.ChatResponse)
async def send_message(request: schemas.ChatRequest):
  try:
    answer = await answer_message(request.message)
  except ValueError:
    raise HTTPException(
      status_code = 503,
      detail = "AI service is unavailable",
    ) from None
  except APITimeoutError:
    raise HTTPException(
      status_code = 504,
      detail = "AI service timed out",
    ) from None
  except (AuthenticationError, RateLimitError):
    raise HTTPException(
      status_code = 503,
      detail = "AI service is temporarily unavailable",
    ) from None
  except APIConnectionError as error:
    cause_type = type(error.__cause__).__name__
    print(f"OpenAI connection failure: {cause_type}")
    raise HTTPException(
      status_code=502,
      detail="Unable to connect to AI service.",
    ) from None
  except APIStatusError as error:
    print(f"OpenAI HTTP failure: {error.status_code}")
    raise HTTPException(
      status_code=502,
      detail="Unable to get a response from AI service.",
    ) from None

  return schemas.ChatResponse(answer = answer)