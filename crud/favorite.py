from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,func
from models.favorite import Favorite
from models.news import News

# 检查收藏状态：当前用户 是否 收藏了这一条新闻，有收藏记录就返回True，没有就返回False
async def is_news_favorited(db: AsyncSession, user_id: int, news_id: int) -> bool:
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    favorite = result.scalar_one_or_none()
    return favorite is not None # 有收藏记录就返回True，没有就返回False


async def add_news_favorite(db:AsyncSession, user_id:int, news_id:int):
    # 检查是否已经收藏过
    if await is_news_favorited(db, user_id, news_id):
        return False  # 已经收藏过，返回False

    new_favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    return new_favorite  # 收藏成功，返回True


async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    query = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0  # 返回是否删除成功


async def get_favorite_list(db: AsyncSession, user_id: int, page: int, page_size: int):
    offset = (page - 1) * page_size # 跳过的记录数
    # 查询得到的结果：[ (News对象, 收藏时间,收藏ID), (News, 。。。), ... ]
    query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
             .join(Favorite, Favorite.news_id == News.id)
             .where(Favorite.user_id == user_id)
             .order_by(Favorite.created_at.desc())
             .offset(offset)
             .limit(page_size)
    )
    result = await db.execute(query)
    # result.all() 返回 [Row(News, favorite_time, favorite_id), ...]
    # 不要用 scalars()，否则会丢掉收藏时间和收藏ID
    favorites = result.all()
    return favorites

async def get_favorite_count(db: AsyncSession, user_id: int):
    query = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    count = result.scalar_one()
    return count


# 清空用户收藏列表：通过user_id来清空对应用户的收藏列表
async def clear_favorite_by_userId(user_id:int, db:AsyncSession):
    query = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount




