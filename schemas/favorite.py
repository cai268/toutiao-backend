from pydantic import BaseModel, Field
from pydantic import ConfigDict
from schemas import base
from datetime import datetime

class FavoriteCheckRequest(BaseModel):
    is_favorited: bool = Field(...,alias='is_favorited',description="是否收藏")  # True表示已收藏，False表示未收藏


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias='news_id', description="新闻ID")  # 新闻ID

# 列表结果
class FavoriteNewsItemResponse(base.NewsBase):
    favorite_id: int = Field(alise= 'favoriteId')
    favorite_time: datetime = Field(alias='favoriteTime')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# 收藏列表响应的模型
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]  # 收藏列表
    total: int = Field(..., description="收藏总数")  # 收藏总数
    has_more: bool = Field(..., description="是否有更多数据")  # 是否有更多数据

    # 模型类的设置
    model_config = ConfigDict(
        populate_by_name=True,  # alias / 字段名兼容
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )