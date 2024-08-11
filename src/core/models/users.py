from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

if TYPE_CHECKING:
    from src.core.models.tweets import Tweet


followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    tweets: Mapped[list["Tweet"]] = relationship("Tweet", back_populates="users")

    # Определяем отношения для следования
    followed_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id,
        back_populates="following_users",
    )

    following_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.followed_id,
        secondaryjoin=id == followers.c.follower_id,
        back_populates="followed_users",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
