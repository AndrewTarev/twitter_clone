from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core import Media, Tweet, User
from src.core.schemas.tweets_schema import AttachmentBase, TweetIn, TweetResponse
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


async def get_all_tweets(user: User, session: AsyncSession):
    stmt = select(Tweet).options(
        selectinload(Tweet.author),
        selectinload(Tweet.media),
        selectinload(Tweet.likes),
    )

    result: Result = await session.execute(stmt)
    tweets = result.scalars().unique().all()

    return tweets
