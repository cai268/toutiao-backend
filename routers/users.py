from fastapi import APIRouter, Depends, Query,HTTPException
from schemas.users import UserRequest, UserResponse_data, UserInfoResponse,UserUpdateRequest,UserUpdatePasswordRequest
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.users import get_user_by_username, create_user, generate_token,authenticate_user,update_user_by_username,update_password
from utils.response import success_response
from utils import auth


router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register")
async def register_user(userdata: UserRequest,db: AsyncSession = Depends(get_db)):#参数需要用户的信息和数据库
    # 注册逻辑：验证用户是否存在，存在则返回错误信息，不存在则创建新用户
    existing_user = await get_user_by_username(db, userdata.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户已存在")

    
    new_user = await create_user(db, userdata.username, userdata.password)
    token = await generate_token(db, new_user.id)

    response_data = UserResponse_data(token=token, userinfo=UserInfoResponse.model_validate(new_user))# 从ORM对象中取值，对应model_config
    return success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login_user(userdata: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await authenticate_user(db, userdata.username, userdata.password)

    if not existing_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = await generate_token(db, existing_user.id)# 验证通过后需要更新token，返回给前端
    response_data = UserResponse_data(token=token, userinfo=UserInfoResponse.model_validate(existing_user))# 从ORM对象中取值，对应model_config
    return success_response(message="登录成功", data=response_data)

@router.get('/info')
async def get_user_info(user = Depends(auth.get_current_user)):

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    response_data = UserInfoResponse.model_validate(user)# 这里不用UserResponse_data，因为前端只需要用户信息，不需要token
    return success_response(message="获取用户信息成功", data=response_data)

# 修改用户信息
@router.put('/update')
async def update_user_info(
    user_update_data: UserUpdateRequest,
    user = Depends(auth.get_current_user), 
    db: AsyncSession = Depends(get_db)

):
    # user = Depends(auth.get_current_user)依赖注入就完成了用户的验证
    
    user = await update_user_by_username(db,user.username,user_update_data)

    response_data = UserInfoResponse.model_validate(user)# 这里不用UserResponse_data，因为前端只需要用户信息，不需要token
    return success_response(message="用户信息更新成功", data=response_data)


# 修改用户密码
@router.put('/password')
async def update_user_password(update_passwords: UserUpdatePasswordRequest,db: AsyncSession = Depends(get_db), user = Depends(auth.get_current_user)):
    # 验证旧密码是否正确
    if not await authenticate_user(db,user.username,update_passwords.old_password):
        raise HTTPException(status_code=400, detail="旧密码错误")

    # 验证新密码和确认密码是否一致
    if update_passwords.new_password != update_passwords.new_password_confirm:
        raise HTTPException(status_code=400, detail="新密码和确认密码不一致")

    # 更新密码
    await update_password(db, user.username, update_passwords.new_password)
    # 返回正确值
    return success_response(message="密码更新成功", data={})




    
    
    