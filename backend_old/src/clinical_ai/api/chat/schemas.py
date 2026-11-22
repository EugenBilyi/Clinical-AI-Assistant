from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
  message: str = Field(min_length=1, max_length=10000)

  model_config = {"str_strip_whitespace": True}

class ChatResponse(BaseModel):
  answer: str