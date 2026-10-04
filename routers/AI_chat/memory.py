from fastapi import APIRouter, Depends

from utils.AI_chat.api_dependencies import get_memory_service
from utils import auth
from schemas.common import (
    ConversationHistory,
    ConversationSummary,
    MessageResponse
)
from AI_models.memory.manager import MemoryManager

router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("", response_model=list[ConversationSummary])
def list_memory(
    user = Depends(auth.get_current_user),
    manager: MemoryManager = Depends(get_memory_service),
) -> list[ConversationSummary]:
    return [
        ConversationSummary(**session)
        for session in manager.list_threads(user.id)
    ]


@router.get("/{dialog_id}/messages", response_model=ConversationHistory)
def get_memory_messages(
    dialog_id: str,
    user = Depends(auth.get_current_user),
    manager: MemoryManager = Depends(get_memory_service),
) -> ConversationHistory:
    return ConversationHistory(
        dialog_id=dialog_id,
        messages=manager.get_messages(user.id, dialog_id),
    )


@router.delete("/{dialog_id}", response_model=MessageResponse)
def delete_memory(
    dialog_id: str,
    user = Depends(auth.get_current_user),
    manager: MemoryManager = Depends(get_memory_service),
) -> MessageResponse:
    manager.clean_thread(user.id, dialog_id)
    return MessageResponse(
        status="ok",
        message=f"已删除对话记忆：{dialog_id}",
    )
