from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    dialog_id: str = Field(min_length=1)
    mode: Literal["rag", "web", "both", "direct", "auto"] = "auto"


class ChatResponse(BaseModel):
    dialog_id: str
    mode: str
    route: str
    query: str
    retrieval: str | None = None
    answer: str
