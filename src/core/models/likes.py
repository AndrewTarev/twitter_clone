from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base

if TYPE_CHECKING:
    from src.core import Tweet, User


class Like(Base):
    __tablename__ = "likes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=False)

    users: Mapped["User"] = relationship(back_populates="likes", single_parent=True)
    tweets: Mapped[List["Tweet"]] = relationship(back_populates="like_relation")

    def __repr__(self) -> str:
        return (
            f"Like(id={self.id!r}, user_id={self.user_id!r}, post_id={self.tweet_id!r})"
        )
