import asyncio
import random

from backend.src.core import Followers, Like, SecurityKey, Tweet, User
from backend.src.core.db_helper import db_helper
from backend.src.utils.logging_config import logger
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

fake = Faker()

NUM_RECORDS = 5
user_list = []
keys_list = []
tweet_list = []
likes_list = []
follower_list = []


async def _create_test_user(session: AsyncSession):
    """Добовляем test в БД, чтобы отработал фронтэнд"""
    test = User(name="test")
    session.add(test)
    await session.flush()
    logger.info(f"User test = {test}")

    test_token = SecurityKey(user_id=test.id, key="test")
    session.add(test_token)
    await session.flush()
    logger.info(f"Api-key for user_test = {test_token}")

    await session.commit()


async def _create_fake_users(session: AsyncSession, num_records: int) -> list[User]:
    """Создаем фэйковых юзеров"""
    for _ in range(num_records):
        fake_name = fake.name()
        new_user = User(name=fake_name)
        user_list.append(new_user)

    session.add_all(user_list)
    logger.info(f"Создан список юзеров {user_list}")
    await session.commit()
    return user_list


async def _create_fake_keys(session: AsyncSession) -> None:
    for user in user_list:
        fake_token = fake.sha1()
        new_token = SecurityKey(user_id=user.id, key=fake_token)
        keys_list.append(new_token)

    session.add_all(keys_list)
    logger.info(f"Создан список ключей {keys_list}")
    await session.commit()


async def _create_fake_tweets(session: AsyncSession):
    """создаем фэйковые твиты"""
    for user in user_list:
        for _ in range(random.randint(1, 5)):
            faker_tweet = fake.text(max_nb_chars=100)
            new_tweet = Tweet(
                author_id=user.id,
                content=faker_tweet,
            )
            tweet_list.append(new_tweet)

    session.add_all(tweet_list)
    logger.info(f"созданы фэйковые твиты = {tweet_list}")
    await session.commit()


async def _create_fake_likes(session: AsyncSession, num_records):
    """Фэйковые лайки"""
    for tweet in tweet_list:
        random_user = random.randint(1, num_records)
        like_relation = Like(user_id=random_user, tweet_id=tweet.id)
        likes_list.append(like_relation)

    session.add_all(likes_list)
    logger.info(likes_list)
    await session.commit()


async def _create_fake_followers(session: AsyncSession):
    """Фэйковые фолловеры"""
    follower_set = set()
    for user in user_list:
        for i in range(random.randint(1, 5)):
            follower_id = random.randint(1, len(user_list) - 1)

            if follower_id != user.id and follower_id not in follower_set:
                follower = Followers(user_id=user.id, follower_id=follower_id)
                session.add(follower)
                follower_set.add(follower_id)

    await session.commit()


async def init_db(session_maker: AsyncSession):
    async with session_maker() as session:
        await _create_test_user(session)
        await _create_fake_users(session=session, num_records=NUM_RECORDS)
        await _create_fake_keys(session)
        await _create_fake_tweets(session)
        await _create_fake_likes(session, num_records=NUM_RECORDS)
        await _create_fake_followers(session)


if __name__ == "__main__":
    asyncio.run(init_db(session_maker=db_helper.session_factory))
