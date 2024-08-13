from fastapi import APIRouter

from src.api.api_v1.routers.tweets import router as tweet_router

router = APIRouter()

router.include_router(tweet_router)
