import json
import sqlite3
from contextlib import closing
from pathlib import Path

from langchain_core.documents import Document

from AI_models.exceptions import KnowledgeBaseError

class ParentDocumentStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        if not self.db_path.exists():
            raise KnowledgeBaseError(
                f"父页数据库不存在：{self.db_path}"
            )
        connection = sqlite3.connect(str(self.db_path))
        connection.row_factory = sqlite3.Row
        return connection

    def find(self, parent_id: str) -> Document | None:
        documents = self.find_many([parent_id])
        return documents.get(parent_id)

    def find_many(self, parent_ids: list[str]) -> dict[str, Document]:
        unique_ids = list(dict.fromkeys(parent_ids))
        if not unique_ids:
            return {}

        placeholders = ",".join("?" for _ in unique_ids)
        with closing(self._connect()) as connection:
            rows = connection.execute(
                f"""
                SELECT parent_id, page_content, metadata_json
                FROM parent_documents
                WHERE parent_id IN ({placeholders})
                """,
                unique_ids,
            ).fetchall()

        return {
            row["parent_id"]: Document(
                page_content=row["page_content"],
                metadata=json.loads(row["metadata_json"]),
            )
            for row in rows
        }

    def replace_for_source(
        self,
        source: str,
        parent_documents: list[Document],
    ) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        rows = [
            (
                document.metadata["parent_id"],
                source,
                document.page_content,
                json.dumps(
                    document.metadata,
                    ensure_ascii=False,
                    default=str,
                ),
            )
            for document in parent_documents
        ]

        with closing(sqlite3.connect(str(self.db_path))) as connection:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS parent_documents (
                        parent_id TEXT PRIMARY KEY,
                        source TEXT NOT NULL,
                        page_content TEXT NOT NULL,
                        metadata_json TEXT NOT NULL
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_parent_documents_source
                    ON parent_documents(source)
                    """
                )
                connection.execute(
                    "DELETE FROM parent_documents WHERE source = ?",
                    (source,),
                )
                connection.executemany(
                    """
                    INSERT OR REPLACE INTO parent_documents
                        (parent_id, source, page_content, metadata_json)
                    VALUES (?, ?, ?, ?)
                    """,
                    rows,
                )
