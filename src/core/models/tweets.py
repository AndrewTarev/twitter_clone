from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

if TYPE_CHECKING:
    from src.core.models.likes import Like
    from src.core.models.medias import Media
    from src.core.models.users import User


class Tweet(Base):
    __tablename__ = "tweets"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # like_id: Mapped[int] = mapped_column(ForeignKey("likes.id"))
    media_id: Mapped[Optional[int]] = mapped_column(ForeignKey("medias.id"))
    content: Mapped[str] = mapped_column(String(3000), nullable=False)
    # likes: Mapped[int] = mapped_column(default=0)
    tweet_date: Mapped[datetime] = mapped_column(server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="tweets", single_parent=True)
    like_relation: Mapped[List["Like"]] = relationship(
        back_populates="tweets", cascade="all, delete-orphan"
    )
    media_path: Mapped["Media"] = relationship(back_populates="tweets")

    def __repr__(self):
        return f"<Post(id={self.id}, content='{self.content}', author_id={self.author_id}, image_path='{self.media_path}')>"
