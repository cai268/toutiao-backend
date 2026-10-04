from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.favorite import is_news_favorited, add_news_favorite,remove_news_favorite,get_favorite_list,get_favorite_count,clear_favorite_by_userId
from schemas.favorite import FavoriteCheckRequest,FavoriteAddRequest,FavoriteListResponse
from utils.response import success_response
from config.db_conf import get_db
from utils import auth


router = APIRouter(prefix="/api/favority", tags=["favority"])


@router.get('/check')
async def check_favority(
    news_id: int = Query(..., description="新闻ID"),
    user = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_favorited = await is_news_favorited(db, user.id, news_id)
    return success_response(message="查询收藏状态成功", data=FavoriteCheckRequest(is_favorited=is_favorited))


@router.post('/add')
async def add_favority(
    news_id: FavoriteAddRequest,
    user = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite = await add_news_favorite(db, user.id, news_id.news_id)

    return success_response(message="收藏成功", data=favorite)


@router.post('/remove')
async def remove_favority(
    news_id: FavoriteAddRequest,
    user = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite = await remove_news_favorite(db, user.id, news_id.news_id)

    return success_response(message="取消收藏成功", data=favorite)


# 获取收藏列表
@router.get('/list')
async def get_favority_list(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    user = Depends(auth.get_current_user)
):
    rows = await get_favorite_list(db, user.id, page, page_size)
    favorite_list = [{
        **news.__dict__,# 将ORM对象转换为字典
        "favorite_time": favorite_time,  # 收藏时间
        "favorite_id": favorite_id  # 收藏ID
    } for news,favorite_time,favorite_id in rows
    ]
    total = await get_favorite_count(db, user.id)
    has_more = total > (page * page_size)  # 是否有更多数据

    data = FavoriteListResponse(list=favorite_list, total=total, has_more=has_more)
    return success_response(message="获取列表收藏成功",
                             data=data
                            )


@router.delete('/clear')
async def clear_favorite(user = Depends(auth.get_current_user),
                         db : AsyncSession = Depends(get_db)
                         ):
    clear_count = await clear_favorite_by_userId(user_id=user.id,db=db)
    if not clear_count:
        raise HTTPException(status_code=400,detail="无收藏列表")

    return success_response(message=f"清空了{clear_count}条收藏记录",data={})

    






