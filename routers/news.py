from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import (
    get_news_count,
    get_news_detail as get_news_detail_record,
    get_news_list,
    get_related_news,
)
from models.news import News, NewsCategory


router = APIRouter(prefix="/api/news", tags=["news"])

# 查询新闻大类
@router.get("/categories")
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(NewsCategory)
        .order_by(NewsCategory.sort_order, NewsCategory.id)
        .offset(skip)
        .limit(limit)
    )
    categories = result.scalars().all()

    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": [
            {
                "id": category.id,
                "name": category.name,
                "sort_order": category.sort_order,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
            }
            for category in categories
        ],
    }


# 查询新闻列表
@router.get("/list")
async def get_new_list(
    category_id: int | None = None,
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    news_list = await get_news_list(
        category_id=category_id,
        page=page,
        page_size=page_size,
        db=db,
    )

    total = await get_news_count(
        db = db,
        category_id = category_id
    )

    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": [
            {
                'list':news_list,
                'total':total
            }
        ],
    }



# 查询新闻详情
@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="ID"),
    db: AsyncSession = Depends(get_db),
):
    news = await get_news_detail_record(news_id, db)

    if news is None:
        return {
            "code": 404,
            "message": "\u65b0\u95fb\u4e0d\u5b58\u5728",
            "data": None,
        }

    recommendations = await get_related_news(
        category_id=news.category_id,
        news_id=news_id,
        db=db,
    )

    return {
        "code": 200,
        "message": "\u83b7\u53d6\u65b0\u95fb\u8be6\u60c5\u6210\u529f",
        "data": {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "category_id": news.category_id,
            "views": news.views,
            "publish_time": news.publish_time,
            "created_at": news.created_at,
            "updated_at": news.updated_at,
            "recommendations": [
                {# 用列表推导式，只拿赋值关键数据
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "image": item.image,
                    "author": item.author,
                    "category_id": item.category_id,
                    "views": item.views,
                    "publish_time": item.publish_time,
                }
                for item in recommendations
            ],
        },
    }
