
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

QuestionText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=1000
    )
]


class ChatRequest(BaseModel):
    question: QuestionText = Field(
        ...,
        description="Student's NPTEL-related question"
    )


class ChatResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    follow_up: str
