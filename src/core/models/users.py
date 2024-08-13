from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

if TYPE_CHECKING:
    from src.core.models.likes import Like
    from src.core.models.tweets import Tweet


followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    # tweet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tweets.id"))
    # like_id: Mapped[Optional[int]] = mapped_column(ForeignKey("likes.id"))

    tweets: Mapped[List["Tweet"]] = relationship(back_populates="author", cascade="all")
    likes: Mapped[List["Like"]] = relationship(back_populates="users", cascade="all")

    # Определяем отношения для следования
    followed_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.follower_id",
        secondaryjoin="User.id == followers.c.followed_id",
        back_populates="following_users",
        cascade="all",
        lazy="selectin",
    )

    following_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.followed_id",
        secondaryjoin="User.id == followers.c.follower_id",
        back_populates="followed_users",
        cascade="all",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
