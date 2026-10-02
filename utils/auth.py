from fastapi import Depends, Query, HTTPException
from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import get_user_by_token
from config.db_conf import get_db

async def get_current_user(
        authorization: str = Header(..., description="Bearer token"),
        db:AsyncSession = Depends(get_db)
):
    # 从Authorization头中提取token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的token格式")
    token = authorization[len("Bearer "):]# 拿到请求头里面的token字段

    user = await get_user_by_token(db, token) # 传入token，并拿取用户信息
    if not user:
        raise HTTPException(status_code=401, detail="无效的token")
    return user