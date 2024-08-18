from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.cruds.tweets_crud import create_new_tweet, get_all_tweets
from src.api.dependencies.user import get_user_dependency
from src.core import User
from src.core.config import settings
from src.core.db_helper import db_helper
from src.core.schemas.error_schemas import ErrorResponse
from src.core.schemas.tweets_schema import TweetIn, TweetOut

router = APIRouter(
    prefix=settings.api.tweets,
    tags=["Tweets"],
    responses={500: {"model": ErrorResponse}},
)


@router.post(
    "",
    response_model=TweetOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_tweets(
    tweet_in: TweetIn,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_user_dependency),
):
    new_tweet = await create_new_tweet(session=session, tweet_in=tweet_in, user=user)
    return {"result": True, "tweet_id": new_tweet.id}


@router.get("")
async def get_tweets(
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    tweets = await get_all_tweets(user=user, session=session)
    return {"result": True, "tweets": tweets}
