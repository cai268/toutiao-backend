from functools import lru_cache

from AI_models.memory.chekpointer import (
    CheckpointerManager,
    get_checkpointer_manager,
)


def build_thread_id(user_id: int, dialog_id: str) -> str:
    if not dialog_id:
        raise ValueError("dialog_id 不能为空")
    return f"user:{user_id}:dialog:{dialog_id}"


def thread_id_prefix(user_id: int) -> str:
    return f"user:{user_id}:dialog:"


class MemoryManager:
    def __init__(
        self,
        checkpointer_manager: CheckpointerManager | None = None,
    ):
        self.checkpointer_manager = (
            checkpointer_manager or get_checkpointer_manager()
        )

    def clean_thread(self, user_id: int, dialog_id: str) -> None:
        thread_id = build_thread_id(user_id, dialog_id)
        self.checkpointer_manager.clean_thread(thread_id)

    def list_threads(self, user_id: int) -> list[dict]:
        return self.checkpointer_manager.list_threads(
            thread_id_prefix(user_id)
        )

    def get_messages(self, user_id: int, dialog_id: str) -> list[dict]:
        thread_id = build_thread_id(user_id, dialog_id)
        return self.checkpointer_manager.get_messages(thread_id)


@lru_cache(maxsize=1)
def get_memory_manager() -> MemoryManager:
    return MemoryManager()


def clean_thread(user_id: int, dialog_id: str) -> None:
    get_memory_manager().clean_thread(user_id, dialog_id)
