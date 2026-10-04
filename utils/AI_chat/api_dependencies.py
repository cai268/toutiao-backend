from functools import lru_cache

from AI_core.pipeline import ChatPipeline
from AI_models.memory.manager import get_memory_manager


@lru_cache(maxsize=1)
def get_pipeline() -> ChatPipeline:
    return ChatPipeline()


def get_memory_service():
    return get_memory_manager()
