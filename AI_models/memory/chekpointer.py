import sqlite3
import threading
from functools import lru_cache
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from config.chat_conf import get_settings
from AI_models.exceptions import ConfigurationError


class CheckpointerManager:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self._lock = threading.Lock()
        self._connection: sqlite3.Connection | None = None
        self._checkpointer: SqliteSaver | None = None

    def _ensure_initialized(self) -> None:
        if self._checkpointer is not None:
            return

        with self._lock:
            if self._checkpointer is not None:
                return

            self.db_path.parent.mkdir(parents=True, exist_ok=True)# 如果文件夹不存在，直接创建
            self._connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
            )
            self._checkpointer = SqliteSaver(self._connection)
            self._checkpointer.setup()

    def get_checkpointer(self) -> SqliteSaver:
        self._ensure_initialized()# 确保已经初始化
        if self._checkpointer is None:
            raise ConfigurationError("checkpointer 初始化失败")
        return self._checkpointer

    def clean_thread(self, thread_id: str) -> None:
        self._ensure_initialized()
        if self._connection is None:
            raise ConfigurationError("记忆数据库连接未初始化")

        with self._lock:
            cursor = self._connection.cursor()
            cursor.execute(
                "DELETE FROM checkpoints WHERE thread_id = ?",
                (thread_id,),
            )
            cursor.execute(
                "DELETE FROM writes WHERE thread_id = ?",
                (thread_id,),
            )
            self._connection.commit()# 将缓存里的事务提交上去，执行后真正删除了数据库的数据

    @staticmethod
    def _message_content(message) -> str:
        content = getattr(message, "content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            return "\n".join(part for part in parts if part)
        return str(content)

    def _messages_for_thread(self, thread_id: str) -> list[dict]:
        item = self.get_checkpointer().get_tuple(
            {"configurable": {"thread_id": thread_id}}
        )
        if item is None:
            return []

        messages = item.checkpoint.get("channel_values", {}).get(
            "messages",
            [],
        )
        role_map = {
            "human": "user",
            "ai": "assistant",
            "system": "system",
        }
        result = []
        for message in messages:
            role = role_map.get(getattr(message, "type", ""))
            if role is None:
                continue
            result.append(
                {
                    "role": role,
                    "content": self._message_content(message),
                }
            )
        return result

    def list_threads(self, thread_id_prefix: str) -> list[dict]:
        if not thread_id_prefix:
            raise ValueError("thread_id_prefix 不能为空")
        self._ensure_initialized()
        if self._connection is None:
            return []

        with self._lock:
            thread_ids = [
                row[0]
                for row in self._connection.execute(
                    (
                        "SELECT DISTINCT thread_id FROM checkpoints "
                        "WHERE thread_id LIKE ?"
                    ),
                    (f"{thread_id_prefix}%",),
                ).fetchall()
            ]

        sessions = []
        for thread_id in thread_ids:
            messages = self._messages_for_thread(thread_id)
            item = self.get_checkpointer().get_tuple(
                {"configurable": {"thread_id": thread_id}}
            )
            first_user_message = next(
                (
                    message["content"]
                    for message in messages
                    if message["role"] == "user"
                ),
                "",
            )
            title = first_user_message.splitlines()[0].strip()
            if title.startswith("用户问题:"):
                title = title.removeprefix("用户问题:").strip()
            if len(title) > 28:
                title = f"{title[:28]}..."

            sessions.append(
                {
                    "dialog_id": thread_id.removeprefix(thread_id_prefix),
                    "title": title or "新会话",
                    "updated_at": (
                        item.checkpoint.get("ts") if item is not None else None
                    ),
                    "message_count": len(messages),
                }
            )

        return sorted(
            sessions,
            key=lambda session: session["updated_at"] or "",
            reverse=True,
        )

    def get_messages(self, thread_id: str) -> list[dict]:
        self._ensure_initialized()
        return self._messages_for_thread(thread_id)

    def close(self) -> None:
        with self._lock:
            if self._connection is not None:
                self._connection.close()
            self._connection = None
            self._checkpointer = None


@lru_cache(maxsize=1)
def get_checkpointer_manager() -> CheckpointerManager:
    return CheckpointerManager(get_settings().memory_db_path)


def get_checkpointer() -> SqliteSaver:
    return get_checkpointer_manager().get_checkpointer()
