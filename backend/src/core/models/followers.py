from backend.src.core.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Followers(Base):
    __tablename__ = "user_following"
    __table_args__ = (
        UniqueConstraint("user_id", "follower_id", name="unique_user_follower_pair"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
