from functools import lru_cache

from langchain_core.documents import Document
from langchain_core.tools import tool

from AI_models.utils.confidence import confidance
from AI_models.utils.rewrite_queries import rewrite_queries
from AI_models.vectorstore.chroma import (
    find_parent_content,
    get_parent_store,
    get_vector_store
)
from AI_models.vectorstore.parent_store import ParentDocumentStore


class RAGService:
    def __init__(
        self,
        vector_store=None,
        parent_store: ParentDocumentStore | None = None,
    ):
        self._vector_store = vector_store
        self._parent_store = parent_store

    @property
    def vector_store(self):
        return self._vector_store or get_vector_store()

    @property
    def parent_store(self) -> ParentDocumentStore:
        if self._parent_store is None:
            self._parent_store = get_parent_store()
        return self._parent_store

    def find_parent_content(
        self,
        respond: list[tuple[Document, float]],
    ) -> list[tuple[Document, float]]:
        return find_parent_content(respond, self.parent_store)

    def search(self, user_query: str) -> str:
        if not user_query:
            return "请输入您的问题"

        try:
            queries = rewrite_queries(user_query) #改写
            best_confidant = 0.0
            best_respond = None
            current_child_respond = None

            for count, query_tmp in enumerate(queries):
                print(f"正在进行第{count + 1}次检索...")
                respond = self.vector_store.similarity_search_with_score(
                    query_tmp,
                    k=4,
                    filter={"retrieval_unit": "child"},
                )
                parent_respond = self.find_parent_content(respond)

                if not parent_respond:
                    return "未找到相关信息，请换个方式提问"

                confidence = confidance(parent_respond)
                if confidence > best_confidant:
                    best_confidant = confidence
                    best_respond = parent_respond[:2]
                    current_child_respond = respond

            if not best_respond or not current_child_respond:
                return "无法检索到答案，请换个提问方式"

            child_doc = current_child_respond[0][0]
            parent_doc = best_respond[0][0]
            page = child_doc.metadata.get("page_number", "?")
            source = child_doc.metadata.get("source", "?")
            content = parent_doc.page_content

            if best_confidant >= 0.7:
                return (
                    f"置信度:{best_confidant * 100:.1f}%，可信度高\n"
                    f"来源：{source}\n页数：{page}\n内容{content}"
                )
            if best_confidant >= 0.4:
                return (
                    f"置信度:{best_confidant * 100:.1f}%，可信度中等\n"
                    f"来源：{source}\n页数：{page}\n内容{content}"
                )
            return (
                f"置信度是{best_confidant * 100:.1f}, 可信度低%,"
                f"来源：{source}\n页数：{page}\n内容{content}"
            )
        except Exception as exc:
            return f"检索失败:{exc}"


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    return RAGService()


@tool
def Get_Notes(user_query: str) -> str:
    """检索本地知识库并返回完整父页内容。"""
    return get_rag_service().search(user_query)
