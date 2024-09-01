from fastapi.security import APIKeyHeader

from backend.src.api.api_v1.cruds.user_crud import get_user
from backend.src.core import User
from backend.src.core.db_helper import db_helper
from fastapi import Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

API_KEY_HEADER = APIKeyHeader(name="api-key")


async def get_user_dependency(
    api_key: str = Security(API_KEY_HEADER),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User | None:
    user = await get_user(session=session, api_key=api_key)
    return user
