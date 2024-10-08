from typing import Sequence

from backend.src.core import Like, Media, Tweet, User
from backend.src.core.schemas.tweets_schema import TweetIn
from backend.src.utils.logging_config import my_logger
from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload


async def create_new_tweet(
    session: AsyncSession, tweet_in: TweetIn, user: User
) -> Tweet:
    tweet: Tweet = Tweet(content=tweet_in.content)
    tweet.author_id = user.id
    session.add(tweet)
    await session.flush()

    my_logger.info(f"Создан твит {tweet}")
    my_logger.info(f"СПИСОК Id МЕДИА - {tweet_in.tweet_media_ids}")
    if tweet_in.tweet_media_ids:
        # Добавление медиафайлов к твиту
        for id_media in tweet_in.tweet_media_ids:
            media_for_update = await session.get(Media, id_media)
            media_for_update.tweet_id = tweet.id  # type: ignore

    await session.commit()

    return tweet


async def get_all_tweets(session: AsyncSession) -> Sequence[Tweet]:
    stmt = select(Tweet).options(
        load_only(Tweet.id, Tweet.content),
        selectinload(Tweet.author),
        selectinload(Tweet.attachments),
        selectinload(Tweet.likes),
    )

    result = await session.execute(stmt)
    tweets: Sequence[Tweet] = result.scalars().all()

    return tweets


async def remove_tweets(session: AsyncSession, tweet_id: int, user: User) -> None:
    tweet = await session.get(Tweet, tweet_id)
    if tweet:
        if tweet.author_id != user.id:
            raise HTTPException(
                status_code=403, detail="You can delete only yourself tweets!"
            )
        await session.delete(tweet)
        await session.commit()


async def add_like_tweets(session: AsyncSession, tweet_id: int, user: User) -> None:
    tweet = await session.get(Tweet, tweet_id)
    if tweet:
        like: Like = Like(user_id=user.id, tweet_id=tweet_id)
        session.add(like)
        await session.commit()
    else:
        raise HTTPException(status_code=400, detail="Tweet not found")


async def remove_like_tweets(session: AsyncSession, tweet_id: int, user: User) -> None:
    tweet = await session.get(Tweet, tweet_id)
    if tweet:
        result = await session.execute(
            select(Like).where(and_(Like.user_id == user.id, Like.tweet_id == tweet_id))
        )
        like = result.scalars().first()
        await session.delete(like)
        await session.commit()
    else:
        raise HTTPException(status_code=400, detail="Tweet not found")
