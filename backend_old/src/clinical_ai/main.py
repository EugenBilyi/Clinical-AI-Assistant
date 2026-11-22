from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from clinical_ai.api.health import router as health_router
from clinical_ai.api.chat.router import router as chat_router

app = FastAPI()
app.include_router(health_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)