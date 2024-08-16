import asyncio
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db_helper
from src.core.models.likes import Like
from src.core.models.security_key import SecurityKey
from src.core.models.tweets import Tweet
from src.core.models.users import User
from src.utils.logging_config import logger

fake = Faker()


async def create_fake_users(session: AsyncSession, num_records=10):
    user_list = []
    for _ in range(num_records):
        fake_name = fake.name()
        new_user = User(name=fake_name)
        logger.info(new_user)
        user_list.append(new_user)
    session.add_all(user_list)
    await session.commit()

    logger.info(user_list)
    return user_list


async def seed_data(session: AsyncSession, num_records=10) -> None:
    # создаем "test"
    test = User(name="test")
    session.add(test)
    await session.flush()
    test_token = SecurityKey(user_id=test.id, key="test")
    session.add(test_token)

    user_list = []

    # создаем юзера
    for _ in range(num_records):
        fake_name = fake.name()
        new_user = User(name=fake_name)
        session.add(new_user)
        await session.flush()
        user_list.append(new_user)

        # создаем api-key для юзера
        fake_token = fake.sha1()
        new_token = SecurityKey(user_id=new_user.id, key=fake_token)
        session.add(new_token)
        await session.flush()

        # создаем твиты для юзера
        for _ in range(random.randint(1, 5)):
            faker_tweet = fake.text(max_nb_chars=100)
            new_tweet = Tweet(
                author_id=new_user.id,
                content=faker_tweet,
            )
            session.add(new_tweet)
            await session.flush()

            # создаем лайки для твита
            like_relation = Like(user_id=new_user.id, tweet_id=new_tweet.id)
            session.add(like_relation)
            await session.flush()

    await session.commit()


async def init_db(session_maker: AsyncSession):
    async with session_maker() as session:
        await seed_data(session, num_records=10)


if __name__ == "__main__":
    asyncio.run(init_db(session_maker=db_helper.session_factory))
