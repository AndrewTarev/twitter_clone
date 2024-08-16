from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base
from src.core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from src.core import Tweet


class Media(Base, IdIntPkMixin):
    __tablename__ = "medias"
    media_path_id: Mapped[int] = mapped_column(nullable=False)

    tweets: Mapped["Tweet"] = relationship(back_populates="media_path")
