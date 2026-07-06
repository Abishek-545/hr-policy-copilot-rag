from pydantic import BaseModel, Field
from fastapi import APIRouter

from services.rag import answer_question

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=600)


@router.post("/chat")
def chat(request: ChatRequest):
    return answer_question(request.question)
