from fastapi import APIRouter
from clinical_ai.api.chat import schemas

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=schemas.ChatResponse)
def send_message(request: schemas.ChatRequest):
  return schemas.ChatResponse(answer=f"Message received: {request.message}")