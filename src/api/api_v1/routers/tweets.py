from fastapi import APIRouter

from src.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.dishes,
    tags=["Dishes"],
)