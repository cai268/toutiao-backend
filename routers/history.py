from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import history
from schemas.history import (
    HistoryAddRequest,
    HistoryAddResponse,
    HistoryListResponse,
)
from utils import auth
from utils.response import success_response


router = APIRouter(prefix="/api/history", tags=["history"])


@router.post('/add')
async def add_history(
    data: HistoryAddRequest,
    user=Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    history_news = await history.add_history_by_newsId(
        db=db,
        user_id=user.id,
        news_id=data.news_id,
    )
    data = HistoryAddResponse.model_validate(history_news)
    return success_response(message="历史记录添加成功", data=data)


@router.get('/list')
async def get_history_list(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    user=Depends(auth.get_current_user),
):
    rows = await history.get_history_list(db, user.id, page, page_size)
    history_list = [{
        **news.__dict__,
        "view_time": view_time,
        "history_id": history_id,
    } for news, view_time, history_id in rows]
    total = await history.get_history_count(db, user.id)
    has_more = total > (page * page_size)

    data = HistoryListResponse(
        list=history_list,
        total=total,
        has_more=has_more,
    )
    return success_response(
        message="获取历史记录列表成功",
        data=data,
    )


# 删除单挑历史记录
@router.delete('/delete/{history_id}')
async def delete_history(
    history_id: int = Path(..., description="历史记录ID"),
    user=Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    deleted = await history.remove_history_by_historyId(
        db=db,
        user_id=user.id,
        history_id=history_id,
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    return success_response(message="删除成功", data={})


# 删除全部历史记录
@router.delete('/clear')
async def clear_history(
    user=Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    clear_count = await history.clear_history_by_userId(
        user_id=user.id,
        db=db,
    )
    if not clear_count:
        raise HTTPException(status_code=400, detail="无历史记录")

    return success_response(
        message=f"清空了{clear_count}条历史记录",
        data={},
    )

