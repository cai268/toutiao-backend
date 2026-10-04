# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
from typing import Any,Optional

from config.redis_conf import get_json_cache, set_cache


CATEGORIES_KEY_PREFIX = "news:categories"
NEWS_LIST = "news_list"
NEWS_DETAIL = "news_detail"


async def _get_news_list_key(categories: Optional[int],page:int, size:int):
    categories = categories if categories is not None else "all"
    key = f"{NEWS_LIST}:{categories}:{page}:{size}"
    return key

async def _get_news_detail_key(news_id:int = 1):
    key = f"{NEWS_DETAIL}:{news_id}"
    return key

# 获取新闻分类缓存
async def get_cache_categories() -> list[dict[str, Any]] | None:
    return await get_json_cache(CATEGORIES_KEY_PREFIX)


# 写入新闻分类缓存：缓存数据，过期时间
async def set_cache_categories(
    data: list[dict[str, Any]],
    expire: int = 7200,
) -> bool:
    return await set_cache(key=CATEGORIES_KEY_PREFIX, value=data, expire=expire)


# 写入缓存-新闻列表,key:new_list:categories:
async def set_cache_news_list(
        categories: Optional[int],
        page:int,
        size:int,
        news_list: list[dict[str,any]],
        expire: int = 600
):
    key = await _get_news_list_key(categories=categories,page=page,size=size)
    return await set_cache(key=key,value=news_list,expire=expire)


# 从缓存中获取新闻列表
async def get_cache_news_list(
        categories:Optional[int],
        page:int,
        size:int,
):
    key = await _get_news_list_key(categories=categories,page=page,size=size)
    return await get_json_cache(key=key)


# 从缓存中拿到新闻详情：参数，新闻ID
async def get_cache_news_detail(news_id: int = 1):
    key = await _get_news_detail_key(news_id=news_id)
    return await get_json_cache(key=key)

async def set_cache_news_detail(news: dict[str,any], news_id: int = 1, expire: int = 600):
    key = await _get_news_detail_key(news_id=news_id)
    return await set_cache(key=key,value=news,expire=expire)

    




