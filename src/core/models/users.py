from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

if TYPE_CHECKING:
    from src.core.models.posts import Post


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("name", "surname", name="unique_name_surname"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, surname={self.surname!r})"
