from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

if TYPE_CHECKING:
    from src.core.models.users import User


class Tweet(Base):
    __tablename__ = "tweets"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(300))
    likes: Mapped[int] = mapped_column(default=0)
    media_path: Mapped[str]
    tweet_data: Mapped[datetime] = mapped_column(default=datetime.now())

    users: Mapped["User"] = relationship(back_populates="tweets")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', author_id={self.author_id}, image_path='{self.media_path}')>"
