from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base

if TYPE_CHECKING:
    from src.core import Tweet


class Media(Base):
    __tablename__ = "medias"
    media_path_id: Mapped[int] = mapped_column(nullable=False)

    tweets: Mapped["Tweet"] = relationship(back_populates="media_path")
