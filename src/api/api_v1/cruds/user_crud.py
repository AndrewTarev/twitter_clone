from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.models.security_key import SecurityKey
from src.core.models.users import User
from src.utils.logging_config import logger


async def get_user(
    session: AsyncSession,
    api_key: str,
) -> User | None:
    stmt = (
        select(User)
        .join(SecurityKey, SecurityKey.user_id == User.id)
        .options(selectinload(User.followers), selectinload(User.following))
        .where(SecurityKey.key == api_key)
    )
    user = await session.execute(stmt)
    result = user.scalars().first()
    logger.info(f"headers api-key: {api_key}")
    logger.info(f"user: {result}")
    return result
