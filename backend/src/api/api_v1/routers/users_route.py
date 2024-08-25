from typing import Annotated

from backend.src.api.api_v1.cruds.user_crud import (
    get_user_by_id_crud,
    user_follow,
    user_unfollow,
)
from backend.src.api.dependencies.user import get_user_dependency
from backend.src.core import User
from backend.src.core.config import settings
from backend.src.core.db_helper import db_helper
from backend.src.core.schemas.users_schema import UserInfoResponse
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix=settings.api.users, tags=["Users"])


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user(user: User = Depends(get_user_dependency)):
    return {"result": True, "user": user}


@router.get("/{id}", response_model=UserInfoResponse)
async def get_user_by_id(
    id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    current_user = await get_user_by_id_crud(session=session, user_id=id)
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": True, "user": current_user}


@router.post("/{id}/follow", status_code=201)
async def follow(
    id: Annotated[int, Path],
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await user_follow(session=session, user_id=id, user=user)
    return {"result": True}


@router.delete("/{id}/follow", status_code=204)
async def unfollow(
    id: Annotated[int, Path],
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await user_unfollow(session=session, user_id=id, user=user)
    return {"result": True}
