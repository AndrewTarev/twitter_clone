from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base
from src.core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from src.core import Tweet


class Media(Base, IdIntPkMixin):
    __tablename__ = "medias"
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=True)
    file_name: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)

    tweets: Mapped["Tweet"] = relationship(back_populates="attachments")
