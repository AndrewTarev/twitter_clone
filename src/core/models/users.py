from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base
from src.core.models.mixins.id_int_pk import IdIntPkMixin
from src.core.models.security_key import SecurityKey

if TYPE_CHECKING:
    from src.core.models.likes import Like
    from src.core.models.tweets import Tweet


class User(Base, IdIntPkMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30), nullable=False)

    tweets: Mapped[List["Tweet"]] = relationship(back_populates="author", cascade="all")
    likes: Mapped[List["Like"]] = relationship(back_populates="users", cascade="all")
    security_keys: Mapped["SecurityKey"] = relationship(
        back_populates="user", cascade="all"
    )

    following = relationship(
        "User",
        secondary="user_following",
        primaryjoin="User.id==user_following.c.user_id",
        secondaryjoin="User.id==user_following.c.follower_id",
        cascade="all",
        lazy="selectin",
        overlaps="followers",
    )
    followers = relationship(
        "User",
        secondary="user_following",
        primaryjoin="User.id==user_following.c.follower_id",
        secondaryjoin="User.id==user_following.c.user_id",
        cascade="all",
        lazy="selectin",
        overlaps="following",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
