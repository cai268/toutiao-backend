import asyncio
import hashlib
import re
import sys
from collections import defaultdict
from collections.abc import Mapping
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_chroma import Chroma
from langchain_core.documents import Document
from sqlalchemy import text

from config.db_conf import AsyncSessionLocal, engine
from AI_models.vectorstore.chroma import get_embeddings
from AI_models.vectorstore.parent_store import ParentDocumentStore

# Chroma 和父页 SQLite 现在都统一使用 VECTOR_DB_DIR，分别生成：
# AI_kb/local_doc_db/chroma.sqlite3
# AI_kb/local_doc_db/parent_documents.sqlite3
VECTOR_DB_DIR = PROJECT_ROOT / "AI_kb" / "local_doc_db"


MAX_CHILD_CHARS = 300
MYSQL_SOURCE_TYPE = "mysql"
MYSQL_PARENT_SOURCE = "mysql://news_app/news"
SENTENCE_END_PATTERN = re.compile(r"(?<=[。.?!！？])")

NEWS_QUERY = text(
    """
    SELECT
        n.id AS news_id,
        n.title,
        n.description,
        n.content,
        n.author,
        n.category_id,
        n.views,
        n.publish_time,
        n.created_at,
        n.updated_at,
        c.name AS category_name,
        c.sort_order AS category_sort_order
    FROM news AS n
    LEFT JOIN news_category AS c
        ON c.id = n.category_id
    ORDER BY n.id
    """
)

RELATED_NEWS_QUERY = text(
    """
    SELECT
        rn.news_id,
        rn.related_news_id,
        n.title AS related_news_title
    FROM related_news AS rn
    LEFT JOIN news AS n
        ON n.id = rn.related_news_id
    ORDER BY rn.news_id, rn.related_news_id
    """
)

FAVORITE_COUNT_QUERY = text(
    """
    SELECT news_id, COUNT(*) AS favorite_count
    FROM favorite
    GROUP BY news_id
    """
)

HISTORY_COUNT_QUERY = text(
    """
    SELECT news_id, COUNT(*) AS history_count
    FROM history
    GROUP BY news_id
    """
)


def _hard_split(text: str, max_chars: int) -> list[str]:
    return [
        text[index:index + max_chars]
        for index in range(0, len(text), max_chars)
    ]


def _split_long_by_sentence(text: str, max_chars: int) -> list[str]:
    chunks = []
    sentences = [
        sentence.strip()
        for sentence in SENTENCE_END_PATTERN.split(text)
        if sentence.strip()
    ]

    for sentence in sentences:
        if len(sentence) <= max_chars:
            chunks.append(sentence)
        else:
            chunks.extend(_hard_split(sentence, max_chars))
    return chunks


def _split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    lines = [line.strip() for line in paragraph.split("\n") if line.strip()]
    if len(lines) <= 1:
        return _split_long_by_sentence(paragraph.strip(), max_chars)

    chunks = []
    for line in lines:
        if len(line) <= max_chars:
            chunks.append(line)
        else:
            chunks.extend(_split_long_by_sentence(line, max_chars))
    return chunks


def split_page_into_children(
    text: str,
    max_chars: int = MAX_CHILD_CHARS,
) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []

    children = []
    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(paragraph) <= max_chars:
            children.append(paragraph)
        else:
            children.extend(_split_long_paragraph(paragraph, max_chars))

    return [child for child in children if child]


def _make_parent_id(source: str, page_number: int) -> str:
    raw = f"{source}\0{page_number}".encode("utf-8")
    return f"page-{hashlib.sha256(raw).hexdigest()[:24]}"


def _make_child_id(parent_id: str, child_index: int) -> str:
    raw = f"{parent_id}\0{child_index}".encode("utf-8")
    return f"child-{hashlib.sha256(raw).hexdigest()[:24]}"


def _string_value(value: object | None, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _datetime_value(value: object | None) -> str:
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return str(value.isoformat())
    return str(value)


def _format_news_page(
    row: Mapping[str, object],
    related_news: list[tuple[int, str]],
    favorite_count: int,
    history_count: int,
) -> str:
    lines = [
        f"标题：{_string_value(row['title'])}",
        f"分类：{_string_value(row['category_name'], '未分类')}",
        f"作者：{_string_value(row['author'], '未知')}",
        f"发布时间：{_datetime_value(row['publish_time'])}",
        f"浏览量：{int(row['views'] or 0)}",
        f"收藏数：{favorite_count}",
        f"浏览历史数：{history_count}",
    ]

    description = _string_value(row["description"]).strip()
    if description:
        lines.extend(["", f"摘要：{description}"])

    content = _string_value(row["content"]).strip()
    lines.extend(["", "正文：", content])

    if related_news:
        lines.extend(["", "相关新闻："])
        lines.extend(
            f"- {news_id}：{title}"
            for news_id, title in related_news
        )

    return "\n".join(lines).strip()


async def _load_mysql_pages() -> list[Document]:
    try:
        async with AsyncSessionLocal() as session:
            news_rows = (await session.execute(NEWS_QUERY)).mappings().all()
            related_rows = (
                await session.execute(RELATED_NEWS_QUERY)
            ).mappings().all()
            favorite_rows = (
                await session.execute(FAVORITE_COUNT_QUERY)
            ).mappings().all()
            history_rows = (
                await session.execute(HISTORY_COUNT_QUERY)
            ).mappings().all()
    finally:
        await engine.dispose()

    related_by_news: dict[int, list[tuple[int, str]]] = defaultdict(list)
    for row in related_rows:
        related_by_news[int(row["news_id"])].append(
            (
                int(row["related_news_id"]),
                _string_value(row["related_news_title"], "未知新闻"),
            )
        )

    favorite_counts = {
        int(row["news_id"]): int(row["favorite_count"])
        for row in favorite_rows
    }
    history_counts = {
        int(row["news_id"]): int(row["history_count"])
        for row in history_rows
    }

    pages = []
    for row in news_rows:
        news_id = int(row["news_id"])
        source = f"{MYSQL_PARENT_SOURCE}/{news_id}"
        related_news = related_by_news.get(news_id, [])

        metadata = {
            "source": source,
            "source_type": MYSQL_SOURCE_TYPE,
            "table": "news",
            "record_id": news_id,
            "news_id": news_id,
            "title": _string_value(row["title"], "无标题"),
            "category_id": int(row["category_id"]),
            "category_name": _string_value(
                row["category_name"],
                "未分类",
            ),
            "category_sort_order": int(
                row["category_sort_order"] or 0
            ),
            "author": _string_value(row["author"], "未知"),
            "views": int(row["views"] or 0),
            "favorite_count": favorite_counts.get(news_id, 0),
            "history_count": history_counts.get(news_id, 0),
            "publish_time": _datetime_value(row["publish_time"]),
            "created_at": _datetime_value(row["created_at"]),
            "updated_at": _datetime_value(row["updated_at"]),
            "related_news_ids": ",".join(
                str(related_id)
                for related_id, _ in related_news
            ),
            "related_news_titles": " | ".join(
                title
                for _, title in related_news
            ),
            "page": 0,
            "page_number": 1,
            "parent_id": _make_parent_id(source, 0),
            "retrieval_unit": "parent",
        }

        pages.append(
            Document(
                page_content=_format_news_page(
                    row,
                    related_news,
                    favorite_counts.get(news_id, 0),
                    history_counts.get(news_id, 0),
                ),
                metadata=metadata,
            )
        )

    return pages


def _add_documents_in_batches(
    vector_store: Chroma,
    documents: list[Document],
    ids: list[str],
) -> None:
    try:
        max_batch_size = int(
            vector_store._collection._client.get_max_batch_size()
        )
    except (AttributeError, TypeError, ValueError):
        max_batch_size = 1000

    batch_size = max(1, min(max_batch_size, 1000))
    total = len(documents)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        vector_store.add_documents(
            documents[start:end],
            ids=ids[start:end],
        )
        print(f"向量写入进度：{end}/{total}")


def build_kb() -> None:
    pages = asyncio.run(_load_mysql_pages())
    if not pages:
        print("MySQL 中未读取到可入库的新闻数据")
        return

    child_documents = []
    child_ids = []
    for page in pages:
        for child_index, child_text in enumerate(
            split_page_into_children(page.page_content, MAX_CHILD_CHARS)
        ):
            child_metadata = dict(page.metadata)
            child_metadata["retrieval_unit"] = "child"
            child_metadata["child_index"] = child_index
            child_documents.append(
                Document(page_content=child_text, metadata=child_metadata)
            )
            child_ids.append(
                _make_child_id(page.metadata["parent_id"], child_index)
            )

    if not child_documents:
        print("未读取到可用于入库的子块")
        return

    output_dir = VECTOR_DB_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    vector_store = Chroma(
        persist_directory=str(output_dir),
        embedding_function=get_embeddings(),
    )

    try:
        vector_store.delete(where={"source_type": MYSQL_SOURCE_TYPE})
        _add_documents_in_batches(
            vector_store,
            child_documents,
            child_ids,
        )
    except Exception:
        vector_store.delete(where={"source_type": MYSQL_SOURCE_TYPE})
        raise

    parent_store = ParentDocumentStore(
        output_dir / "parent_documents.sqlite3"
    )
    parent_store.replace_for_source(MYSQL_PARENT_SOURCE, pages)
    print(
        f"知识库构建完成，共入库 {len(pages)} 个新闻父页、"
        f"{len(child_documents)} 个子块"
    )


if __name__ == "__main__":
    build_kb()
