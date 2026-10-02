from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func,UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from config.db_conf import Base


class History(Base):
    __tablename__ = "history"

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
    view_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
                    "user_id",
                    "news_id",
                    name="user_news_unique",
                ),
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
        Index("idx_view_time", view_time.desc()),
    )
