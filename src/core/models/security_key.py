from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base
from src.core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models.users import User


class SecurityKey(Base, IdIntPkMixin):
    __tablename__ = "security_key"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    key: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    user: Mapped["User"] = relationship(
        back_populates="security_keys", single_parent=True
    )
