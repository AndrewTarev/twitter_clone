from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core import Followers
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


async def get_user_by_id_crud(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    stmt = (
        select(User)
        .options(selectinload(User.followers))
        .options(selectinload(User.following))
        .where(User.id == user_id)
    )
    user = await session.execute(stmt)
    user = user.scalars().first()
    return user


async def user_follow(
    session: AsyncSession,
    user_id: int,
    user: User,
):
    try:
        follow: Followers = Followers(user_id=user.id, follower_id=user_id)
        session.add(follow)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Follow already exists")


async def user_unfollow(
    session: AsyncSession,
    user_id: int,
    user: User,
) -> None:
    stmt = select(Followers).where(
        and_(Followers.user_id == user.id, Followers.follower_id == user_id)
    )
    result = await session.execute(stmt)
    follow = result.scalars().first()
    logger.info(f"follow: {follow}")

    if follow:
        await session.delete(follow)
        await session.commit()
