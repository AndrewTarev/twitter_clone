from fastapi import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload

from src.core import Media, Tweet, User
from src.core.schemas.tweets_schema import TweetIn
from src.utils.logging_config import logger


async def create_new_tweet(
    session: AsyncSession, tweet_in: TweetIn, user: User
) -> Tweet:
    tweet: Tweet = Tweet(content=tweet_in.content)
    tweet.author_id = user.id
    session.add(tweet)
    await session.flush()

    logger.info(f"Создан твит {tweet}")
    logger.info(f"СПИСОК Id МЕДИА - {tweet_in.tweet_media_ids}")
    if tweet_in.tweet_media_ids:
        # Добавление медиафайлов к твиту
        for id_media in tweet_in.tweet_media_ids:
            media_for_update = await session.get(Media, id_media)
            media_for_update.tweet_id = tweet.id
            logger.info(
                f"Привязал медиа к твиту - Media.tweet_id={media_for_update.tweet_id}"
            )

    await session.commit()

    return tweet


async def get_all_tweets(session: AsyncSession):
    stmt = (
        select(Tweet)
        .options(
            load_only(Tweet.id, Tweet.content),
            selectinload(Tweet.author),
        )
        .options(selectinload(Tweet.attachments))
        .options(selectinload(Tweet.likes))
    )

    result: Result = await session.execute(stmt)
    tweets = result.scalars().unique().all()

    return tweets


async def remove_tweets(session: AsyncSession, tweet_id: int, user: User):
    tweet = await session.get(Tweet, tweet_id)
    if tweet.author_id != user.id:
        raise HTTPException(
            status_code=403, detail="You can delete only yourself tweets!"
        )
    await session.delete(tweet)
    await session.commit()
