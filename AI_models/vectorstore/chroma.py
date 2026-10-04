from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config.chat_conf import get_settings
from AI_models.exceptions import ConfigurationError,KnowledgeBaseError
from AI_models.vectorstore.parent_store import ParentDocumentStore


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model_name,
        model_kwargs={"device": settings.embedding_device},
    )


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    settings = get_settings()
    persist_directory = settings.vectorstore_read_dir
    if not (persist_directory / "chroma.sqlite3").exists():
        raise KnowledgeBaseError(
            f"Chroma 数据库不存在：{persist_directory}。"
            "请先运行 python -m AI_models.build_kb"
        )

    return Chroma(
        persist_directory=str(persist_directory),
        embedding_function=get_embeddings(),
    )


def get_parent_store() -> ParentDocumentStore:
    settings = get_settings()
    return ParentDocumentStore(settings.parent_db_read_path)


def find_parent_content(
    respond: list[tuple[Document, float]],
    parent_store: ParentDocumentStore | None = None,
) -> list[tuple[Document, float]]:
    parent_store = parent_store or get_parent_store()
    parent_ids = [
        child_doc.metadata.get("parent_id")
        for child_doc, _ in respond
        if child_doc.metadata.get("parent_id")
    ]
    parent_map = parent_store.find_many(parent_ids)

    parent_respond = []
    seen = set()
    for child_doc, score in respond:
        parent_id = child_doc.metadata.get("parent_id")
        if not parent_id or parent_id in seen or parent_id not in parent_map:
            continue
        seen.add(parent_id)
        parent_respond.append((parent_map[parent_id], score))

    return parent_respond


def similarity_search_children(
    query: str,
    k: int = 4,
) -> list[tuple[Document, float]]:
    if not query:
        raise ConfigurationError("检索问题不能为空")
    return get_vector_store().similarity_search_with_score(
        query,
        k=k,
        filter={"retrieval_unit": "child"},
    )
