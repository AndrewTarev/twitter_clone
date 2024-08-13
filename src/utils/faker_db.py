import asyncio
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import Like, Tweet, User
from src.core.db_helper import db_helper

fake = Faker()


async def seed_data(session: AsyncSession, num_records=100) -> None:
    for _ in range(num_records):
        fake_name = fake.name()
        new_record = User(name=fake_name)
        session.add(new_record)
        await session.flush()

        print(new_record)
        for _ in range(random.randint(1, 5)):
            faker_tweet = fake.text(max_nb_chars=100)
            new_tweet = Tweet(
                author_id=new_record.id,
                content=faker_tweet,
            )
            session.add(new_tweet)
            await session.flush()

            like_relation = Like(user_id=new_record.id, tweet_id=new_tweet.id)
            session.add(like_relation)
            await session.flush()

    await session.commit()


async def init_db(session_maker: AsyncSession):
    async with session_maker() as session:
        await seed_data(session, num_records=100)


if __name__ == "__main__":
    asyncio.run(init_db(session_maker=db_helper.session_factory))
