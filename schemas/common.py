from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str


class MessageResponse(BaseModel):
    status: str
    message: str


class ConversationSummary(BaseModel):
    dialog_id: str
    title: str
    updated_at: str | None = None
    message_count: int


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ConversationHistory(BaseModel):
    dialog_id: str
    messages: list[ConversationMessage]