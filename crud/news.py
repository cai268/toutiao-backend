from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import News, NewsCategory


async def get_news_categories(
    db: AsyncSession,
    category_id: int | None = None,
    page: int = 1,
    page_size: int = 10,
) -> list[NewsCategory]:
    statement = select(NewsCategory)

    if category_id is not None:
        statement = statement.where(NewsCategory.id == category_id)

    statement = (
        statement.order_by(NewsCategory.sort_order, NewsCategory.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(statement)
    return list(result.scalars().all())


async def get_news_list(
    category_id: int | None,
    page: int,
    page_size: int,
    db: AsyncSession,
) -> list[News]:
    statement = select(News)

    if category_id is not None:
        statement = statement.where(News.category_id == category_id)

    statement = (
        statement.order_by(News.publish_time.desc(), News.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(statement)
    return list(result.scalars().all())


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


async def get_news_detail(
    news_id: int,
    db: AsyncSession,
) -> News | None:
    result = await db.execute(
        select(News).where(News.id == news_id)
    )
    news = result.scalar_one_or_none()

    if news is None:
        return None

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
    return news


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
