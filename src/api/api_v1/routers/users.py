from fastapi import APIRouter, Depends

from src.api.dependencies.user import get_user_dependency
from src.core import User
from src.core.config import settings
from src.core.schemas.users_schema import UserInfoResponse

router = APIRouter(
    prefix=settings.api.users,
    tags=["Users"],
)


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user(user: User = Depends(get_user_dependency)):
    return {"result": True, "user": user}
