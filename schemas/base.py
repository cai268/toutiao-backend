from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class NewsBase(BaseModel):
    id:int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views:int
    publish_time: Optional[datetime] = Field(None,alias='publishedTime')

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: str
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
