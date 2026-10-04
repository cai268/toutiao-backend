from pydantic import BaseModel, Field
from pydantic import ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str
# 用户信息的基础模型 + 用户信息的响应模型
class UserInfoBase(BaseModel):
    bio: str | None = None
    avatar: str | None = None
    nickname: str | None = None
    gender: str | None = None

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类的设置
    model_config = ConfigDict(
        populate_by_name=True,  # alias / 字段名兼容
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )


# data类型
class UserResponse_data(BaseModel):
    token: str
    userinfo : UserInfoResponse = Field(..., alias="userinfo")# 设置别名

    # 模型类的设置
    model_config = ConfigDict(
        populate_by_name=True,  # alias / 字段名兼容
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )


# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: str | None = None
    avatar: str | None = Field(default=None, max_length=255)
    bio: str | None = None
    gender: str | None = None


# 更新用户密码的模型类
class UserUpdatePasswordRequest(BaseModel):
    old_password:str = Field(..., description="旧密码")
    new_password:str = Field(..., description="新密码")
    new_password_confirm:str = Field(..., description="确认新密码")
