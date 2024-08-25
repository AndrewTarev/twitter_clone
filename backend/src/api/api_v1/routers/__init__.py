from backend.src.api.api_v1.routers.media_route import router as media_router
from backend.src.api.api_v1.routers.tweets_route import router as tweet_router
from backend.src.api.api_v1.routers.users_route import router as user_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(tweet_router)
router.include_router(user_router)
router.include_router(media_router)
