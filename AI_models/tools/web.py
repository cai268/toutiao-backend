from functools import lru_cache

import requests
from langchain_core.tools import tool

from config.chat_conf import get_settings
from AI_models.utils.cleaner import clear_data


class BochaSearchService:
    def __init__(
        self,
        api_key: str | None = None,
        session=None,
    ):
        settings = get_settings()
        self.api_key = api_key if api_key is not None else settings.bocha_api_key
        self.session = session or requests

    def search(self, user_query: str, count: int = 5) -> str:
        if not user_query:
            return "请提供搜索关键词"
        if not self.api_key:
            return "搜索失败: 未配置 BOCHA_API_KEY"

        try:
            response = self.session.post(
                "https://api.bocha.cn/v1/web-search",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "query": user_query,
                    "freshness": "oneYear",
                    "summary": True,
                    "count": count,
                },
                timeout=15,
            )

            if response.status_code != 200:
                return f"搜索请求失败，状态码: {response.status_code}"

            data = response.json()
            webpages = (
                data.get("data", {})
                .get("webPages", {})
                .get("value", [])
            )
            if not webpages:
                return f"未搜索到关于“{user_query}”的结果，请更换关键词"

            results = []
            for index, page in enumerate(webpages, start=1):
                title = clear_data(page.get("name", ""))
                link = page.get("url", "")
                summary = clear_data(
                    page.get("summary", "") or page.get("snippet", "")
                )
                date = page.get("datePublished", "")
                results.append(
                    f"【{index}】{title}\n"
                    f"链接：{link}\n摘要：{summary}\n时间：{date}"
                )

            return "\n\n".join(results)
        except requests.exceptions.Timeout:
            return "搜索请求超时，请稍后重试"
        except Exception as exc:
            return f"搜索失败: {exc}"


@lru_cache(maxsize=1)
def get_web_service() -> BochaSearchService:
    return BochaSearchService()


@tool
def Bocha_Search(user_query: str, count: int = 5) -> str:
    """使用博查搜索获取知识库外的信息。"""
    return get_web_service().search(user_query, count)