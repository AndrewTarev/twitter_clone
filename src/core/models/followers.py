from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class Followers(Base):
    __tablename__ = "user_following"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
