from typing import Annotated

from backend.src.api.api_v1.cruds.user_crud import get_user
from backend.src.core import User
from backend.src.core.db_helper import db_helper
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_dependency(
    api_key: Annotated[str | None, Header()],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await get_user(session=session, api_key=api_key)
    return user
