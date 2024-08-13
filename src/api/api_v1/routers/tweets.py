from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.cruds.tweets_crud import create_new_tweet
from src.core import Tweet
from src.core.config import settings
from src.core.db_helper import db_helper
from src.core.schemas.tweets_schema import TweetIn, TweetOut

router = APIRouter(
    prefix=settings.api.tweets,
    tags=["Tweets"],
)


@router.post(
    "",
    response_model=TweetOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_tweets(
    tweet_in: TweetIn,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Tweet:
    return await create_new_tweet(session=session, tweet_in=tweet_in)
