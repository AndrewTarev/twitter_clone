from typing import Annotated, Any, Dict

from backend.src.api.api_v1.cruds.tweets_crud import (
    add_like_tweets,
    create_new_tweet,
    get_all_tweets,
    remove_like_tweets,
    remove_tweets,
)
from backend.src.api.dependencies.user import get_user_dependency
from backend.src.core import User
from backend.src.core.config import settings
from backend.src.core.db_helper import db_helper
from backend.src.core.schemas.tweets_schema import TweetIn, TweetOut, TweetsResponseOut
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

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
    user: User = Depends(get_user_dependency),
) -> Dict[str, Any]:
    new_tweet = await create_new_tweet(session=session, tweet_in=tweet_in, user=user)
    return {"result": True, "tweet_id": new_tweet.id}


@router.get(
    "",
    response_model=TweetsResponseOut,
)
async def get_tweets(
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Dict[str, Any]:
    tweets = await get_all_tweets(session=session)
    return {"result": True, "tweets": tweets}


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
async def delete_tweets(
    id: Annotated[int, Path],
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
):  # type: ignore
    await remove_tweets(session=session, tweet_id=id, user=user)
    return {"result": True}


@router.post("/{id}/likes", status_code=status.HTTP_201_CREATED)
async def like_tweets(
    id: Annotated[int, Path],
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Dict[str, bool]:
    await add_like_tweets(session=session, tweet_id=id, user=user)
    return {"result": True}


@router.delete(
    "/{id}/likes",
    status_code=status.HTTP_200_OK,
)
async def delete_like_tweets(
    id: Annotated[int, Path],
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
):  # type: ignore
    await remove_like_tweets(session=session, tweet_id=id, user=user)
    return {"result": True}
