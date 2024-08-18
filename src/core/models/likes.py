from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base
from src.core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from src.core import Tweet, User


class Like(Base, IdIntPkMixin):
    __tablename__ = "likes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=False)

    users: Mapped["User"] = relationship(back_populates="like_user", single_parent=True)
    tweets: Mapped[List["Tweet"]] = relationship(back_populates="likes")

    def __repr__(self) -> str:
        return f"Like(id={self.id!r}, user_id={self.user_id!r}, tweet_id={self.tweet_id!r})"
