# 根据用户名查询用户
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models.users import User, UserToken
from utils import security
from schemas.users import UserUpdateRequest
from fastapi import HTTPException
import datetime
import uuid

# 根据用户名查询用户,查询用户是否存在
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)# 这仅仅只是构建查询对象，并没有真正查询数据
    result = await db.execute(query)# 真正查询数据，根据上面的查询语句
    return result.scalar_one_or_none()# 获取查询结果，如果没有查询到数据，则返回None

# 创建用户
async def create_user(db: AsyncSession, username: str, password: str):
    secure_password = security.get_hash_password(password)# 对密码进行加密
    new_user = User(username=username, password=secure_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)# 刷新对象，获取数据库中最新的数据
    return new_user

# 生成token
async def generate_token(db: AsyncSession, user_id: int):
    # 生成token+设置过期时间 ->查询数据库当前用户是否有token -> 有:更新；没有:创建
    token = str(uuid.uuid4())  # 生成随机token
    # 设置过期时间
    expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=5)  # 设置过期时间为5小时后

    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 存在则更新时间和token
        user_token.token = token
        user_token.expires_at = expire_time
    else:
        # 不存在就创建
        new_token = UserToken(user_id=user_id, token=token, expires_at=expire_time)
        db.add(new_token)

    await db.commit()

    return token

# 验证用户身份，判断登录账号和密码是否正确
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

# 查看用户信息:验证token是否有效 -> 有效则返回用户信息，无效则返回None
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    # 检查token是否存在
    # 检查token是否过期
    if not user_token :
        return None

    expires_at = user_token.expires_at

    if expires_at.tzinfo is None:# 如果没有时区，就补上
        expires_at = expires_at.replace(tzinfo=datetime.UTC)

    if expires_at <= datetime.datetime.now(datetime.UTC):
        return None

    query = select(User).where(User.id == user_token.user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user

# 修改用户信息
async def update_user_by_username(db: AsyncSession, username: str, update_user_data:UserUpdateRequest):
    # 先检查用户是否存在
    query_select = select(User).where(User.username == username)
    result = await db.execute(query_select)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 用户存在再更新用户
    # query = update(User).where(User.username == username).values(# 更新:字段=值)
    # update_user_data是pydantic类型，可以将它先转为字典，然后解包就可以获得字段=值，字段=值的类型
    query = update(User).where(User.username == username).values(
        **update_user_data.model_dump(exclude_unset=True,exclude_none=True)
        )
    await db.execute(query)
    await db.commit()

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    return user

# 更新用户密码
async def update_password(db: AsyncSession, username: str, new_password: str):
    secure_password = security.get_hash_password(new_password)# 对密码进行加密

    result = await db.execute(
        select(User)
        .where(User.username == username)
    )
    user = result.scalar_one_or_none()

    user.password = secure_password

    await db.commit()
    await db.refresh(user)
    return user