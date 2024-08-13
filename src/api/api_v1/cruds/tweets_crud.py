from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import Tweet
from src.core.schemas.tweets_schema import TweetIn


async def create_new_tweet(
    session: AsyncSession,
    tweet_in: TweetIn,
) -> Tweet:
    tweet: Tweet = Tweet(**tweet_in.model_dump())
    session.add(tweet)
    await session.commit()
    return tweet
