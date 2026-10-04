from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.encoders import jsonable_encoder
from schemas.base import NewsBase,NewsResponse
from cache.news_cache import get_cache_categories, set_cache_categories,set_cache_news_list,get_cache_news_list,get_cache_news_detail,set_cache_news_detail
from models.news import News, NewsCategory
import json

# 得到新闻分类
async def get_news_categories(
    db: AsyncSession,
    category_id: int | None = None,
    page: int = 1,
    page_size: int = 10,
    *,
    skip: int | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    offset = skip if skip is not None else (page - 1) * page_size
    result_limit = limit if limit is not None else page_size

    # 先从缓存中读取数据
    cache_categories = await get_cache_categories()
    if cache_categories is not None:
        return cache_categories

    # 缓存未命中时从数据库获取
    statement = select(NewsCategory)
    if category_id is not None:
        statement = statement.where(NewsCategory.id == category_id)

    statement = (
        statement.order_by(NewsCategory.sort_order, NewsCategory.id)
        .offset(offset)
        .limit(result_limit)
    )

    result = await db.execute(statement)
    categories = [
        {
            "id": category.id,
            "name": category.name,
            "sort_order": category.sort_order,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
        for category in result.scalars().all()
    ]


    # 写入缓存
    categories = jsonable_encoder(categories)
    await set_cache_categories(
        data=categories
    )

    return categories


# 读取新闻列表
async def get_news_list(
    category_id: int | None,
    page: int,
    page_size: int,
    db: AsyncSession,
) -> list[News]:
    # 先从缓存里面取
    cache_list = await get_cache_news_list(categories=category_id,page=page,size=page_size)

    if cache_list:
        return [News(**item) for item in cache_list]

    # 从数据库中查找
    statement = select(News)
    if category_id is not None:
        statement = statement.where(News.category_id == category_id)

    statement = (
        statement.order_by(News.publish_time.desc(), News.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(statement)
    news_list = result.scalars().all()

    # 未命中，再写入缓存
    if news_list:
        # 先把ORM数据转化成字典才能写入缓存
        # ORM 转为 Pydantic，再转为字典
        news_data = [NewsBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        await set_cache_news_list(category_id,page,page_size,news_data)

    return news_list


async def get_news_count(
    db: AsyncSession,
    category_id: int,
) -> int:
    statement = (
        select(func.count(News.id))
        .select_from(News)
        .where(News.category_id == category_id)
    )
    result = await db.execute(statement)
    return int(result.scalar_one())


# 获取新闻并更新新闻的浏览量
async def get_news_detail(
    news_id: int,
    db: AsyncSession,
) -> News | None:
    # 先从缓存中拿到新闻详情
    cache_detail = await get_cache_news_detail(news_id=news_id)
    if cache_detail is not None:

        news = News(**cache_detail) 
        return news

    # 未命中
    result = await db.execute(
        select(News).where(News.id == news_id)
    )
    news = result.scalar_one_or_none()

    if news is None:
        return None
    # 更新新闻的浏览量
    try:
        await db.execute(
            update(News)
            .where(News.id == news_id)
            .values(views=News.views + 1)
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(news)
    # return news

    # 写入缓存
    news_data = NewsResponse.model_validate(news).model_dump(mode="json",by_alias=False)
    await set_cache_news_detail(news=news_data,news_id=news_id) 
    
    return news


# 获取相似的新闻
async def get_related_news(
    category_id: int,
    news_id: int,
    db: AsyncSession,
) -> list[News]:
    result = await db.execute(
        select(News)
        .where(
            News.category_id == category_id,
            News.id != news_id,
        )
        .order_by(
            News.views.desc(),
            News.publish_time.desc(),
            News.id.desc(),
        )
        .limit(2)
    )
    return list(result.scalars().all())
