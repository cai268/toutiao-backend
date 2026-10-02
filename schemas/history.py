from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas import base


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

    model_config = ConfigDict(populate_by_name=True)


class HistoryAddResponse(BaseModel):
    id: int
    user_id: int = Field(alias="userId")
    news_id: int = Field(alias="newsId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class HistoryNewsItemResponse(base.NewsBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
