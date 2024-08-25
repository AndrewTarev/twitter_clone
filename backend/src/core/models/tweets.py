from typing import TYPE_CHECKING, List

from backend.src.core.base import Base
from backend.src.core.models.mixins.id_int_pk import IdIntPkMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from backend.src import Like, Media, User


class Tweet(Base, IdIntPkMixin):
    __tablename__ = "tweets"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String(3000), nullable=False)

    author: Mapped["User"] = relationship(back_populates="tweets", single_parent=True)
    likes: Mapped[List["Like"]] = relationship(
        back_populates="tweets", cascade="all, delete-orphan"
    )
    attachments: Mapped[List["Media"]] = relationship(
        back_populates="tweets", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tweet(id={self.id}, content={self.content}, author={self.author})>"
