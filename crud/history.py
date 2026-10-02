import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


# Add a history record, or refresh view_time when it already exists.
async def add_history_by_newsId(db: AsyncSession, user_id: int, news_id: int):
    query = select(History).where(
        History.user_id == user_id,
        History.news_id == news_id,
    )
    result = await db.execute(query)
    history = result.scalar_one_or_none()

    if history:
        history.view_time = datetime.datetime.now(datetime.UTC)
    else:
        history = History(
            user_id=user_id,
            news_id=news_id,
            view_time=datetime.datetime.now(datetime.UTC),
        )
        db.add(history)

    await db.commit()
    await db.refresh(history)
    return history


# 删除单条历史记录
async def remove_history_by_historyId(
    db: AsyncSession,
    user_id: int,
    history_id: int,
):
    query = delete(History).where(
        History.id == history_id,
        History.user_id == user_id,
    )
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0


# 获得历史记录列表
async def get_history_list(
    db: AsyncSession,
    user_id: int,
    page: int,
    page_size: int,
):
    offset = (page - 1) * page_size
    query = (
        select(
            News,
            History.view_time.label("view_time"),
            History.id.label("history_id"),
        )
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    return result.all()


# 计算历史记录数量
async def get_history_count(db: AsyncSession, user_id: int):
    query = select(func.count(History.id)).where(History.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one()

# 删除某用户的全部历史记录
async def clear_history_by_userId(user_id: int, db: AsyncSession):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount
