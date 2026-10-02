from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from config.db_conf import Base


class Favorite(Base):
    __tablename__ = "favorite"
    __table_args__ = (
        # UniqueConstraint：唯一约束，当前用户，当前新闻，只能收藏一次
        UniqueConstraint(
            "user_id",
            "news_id",
            name="user_news_unique",
        ),
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
    )

    id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    news_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey(
            "news.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
