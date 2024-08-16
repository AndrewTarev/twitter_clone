from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.cruds.user_crud import get_user
from src.core.db_helper import db_helper


async def get_user_dependency(
    api_key: Annotated[str | None, Header()],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user = await get_user(session=session, api_key=api_key)
    return user
