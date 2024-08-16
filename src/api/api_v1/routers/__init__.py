from fastapi import APIRouter

from src.api.api_v1.routers.tweets import router as tweet_router
from src.api.api_v1.routers.users import router as user_router

router = APIRouter()

router.include_router(tweet_router)
router.include_router(user_router)
