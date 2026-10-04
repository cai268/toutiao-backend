import json
from collections.abc import Iterator
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from utils.AI_chat.api_dependencies import get_pipeline
from utils import auth
from schemas.chat import ChatRequest, ChatResponse
from AI_core.pipeline import ChatPipeline


router = APIRouter(prefix="/api/chat", tags=["chat"])


def _format_sse(event: str, data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user = Depends(auth.get_current_user),
    pipeline: ChatPipeline = Depends(get_pipeline),
) -> ChatResponse:
    return pipeline.chat(request, user.id)


@router.post("/stream")
def chat_stream(
    request: ChatRequest,
    user=Depends(auth.get_current_user),
    pipeline: ChatPipeline = Depends(get_pipeline),
) -> StreamingResponse:
    def event_stream() -> Iterator[str]:
        for event in pipeline.stream(request, user.id):
            yield _format_sse(event["event"], event["data"])

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
