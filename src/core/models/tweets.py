from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models.likes import Like
    from src.core.models.medias import Media
    from src.core.models.users import User


class Tweet(Base, IdIntPkMixin):
    __tablename__ = "tweets"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String(3000), nullable=False)

    author: Mapped["User"] = relationship(back_populates="tweets", single_parent=True)
    likes: Mapped[List["Like"]] = relationship(
        back_populates="tweets", cascade="all, delete-orphan"
    )
    media: Mapped[List["Media"]] = relationship(
        back_populates="tweets", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tweet(id={self.id}, content='{self.content}', author_id={self.author_id}')>"
