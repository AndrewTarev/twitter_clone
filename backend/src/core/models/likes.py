from typing import TYPE_CHECKING, List

from backend.src.core.base import Base
from backend.src.core.models.mixins.id_int_pk import IdIntPkMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from backend.src.core import Tweet, User


class Like(Base, IdIntPkMixin):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "tweet_id", name="unique_user_tweet_pair"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=False)

    users: Mapped["User"] = relationship(back_populates="like_user", single_parent=True)
    tweets: Mapped[List["Tweet"]] = relationship(back_populates="likes")

    def __repr__(self) -> str:
        return f"Like(id={self.id!r}, user_id={self.user_id!r}, tweet_id={self.tweet_id!r})"
