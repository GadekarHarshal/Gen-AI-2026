
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Student's NPTEL-related question"
    )


class ChatResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    follow_up: str
