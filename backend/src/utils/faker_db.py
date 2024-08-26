import asyncio
import random

from backend.src.core import Followers, Like, SecurityKey, Tweet, User
from backend.src.core.db_helper import db_helper
from backend.src.utils.logging_config import logger
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

fake = Faker()


class FakeData:
    def __init__(self, session: AsyncSession, num_records: int):
        self.num_records: int = num_records
        self.session: AsyncSession = session
        self.user_list = []
        self.keys_list = []
        self.tweet_list = []
        self.likes_list = []
        self.follower_list = []

    async def _create_test_user(self):
        """Добовляем test в БД, чтобы отработал фронтэнд"""
        test = User(name="test")
        self.session.add(test)
        await self.session.flush()
        logger.info(f"User test = {test}")

        test_token = SecurityKey(user_id=test.id, key="test")
        self.session.add(test_token)
        await self.session.flush()
        logger.info(f"Api-key for user_test = {test_token}")

        await self.session.commit()

    async def _create_fake_users(self) -> list[User]:
        """Создаем фэйковых юзеров"""
        for _ in range(self.num_records):
            fake_name = fake.name()
            new_user = User(name=fake_name)
            self.user_list.append(new_user)

        self.session.add_all(self.user_list)
        logger.info(f"Создан список юзеров {self.user_list}")
        await self.session.commit()
        return self.user_list

    async def _create_fake_keys(self) -> None:
        for user in self.user_list:
            fake_token = fake.sha1()
            new_token = SecurityKey(user_id=user.id, key=fake_token)
            self.keys_list.append(new_token)

        self.session.add_all(self.keys_list)
        logger.info(f"Создан список ключей {self.keys_list}")
        await self.session.commit()

    async def _create_fake_tweets(self):
        """создаем фэйковые твиты"""
        for user in self.user_list:
            for _ in range(random.randint(1, 5)):
                faker_tweet = fake.text(max_nb_chars=100)
                new_tweet = Tweet(
                    author_id=user.id,
                    content=faker_tweet,
                )
                self.tweet_list.append(new_tweet)

        self.session.add_all(self.tweet_list)
        logger.info(f"созданы фэйковые твиты = {self.tweet_list}")
        await self.session.commit()

    async def _create_fake_likes(self):
        """Фэйковые лайки"""
        for tweet in self.tweet_list:
            random_user = random.randint(1, self.num_records)
            like_relation = Like(user_id=random_user, tweet_id=tweet.id)
            self.likes_list.append(like_relation)

        self.session.add_all(self.likes_list)
        logger.info(self.likes_list)
        await self.session.commit()

    async def _create_fake_followers(self):
        """Фэйковые фолловеры"""
        follower_set = set()
        for user in self.user_list:
            for i in range(random.randint(1, 5)):
                follower_id = random.randint(1, len(self.user_list) - 1)

                if follower_id != user.id and follower_id not in follower_set:
                    follower = Followers(user_id=user.id, follower_id=follower_id)
                    self.session.add(follower)
                    follower_set.add(follower_id)

        await self.session.commit()

    async def __call__(self):
        await self._create_test_user()
        await self._create_fake_users()
        await self._create_fake_keys()
        await self._create_fake_tweets()
        await self._create_fake_likes()
        await self._create_fake_followers()


async def main():
    async with db_helper.session_factory() as session:
        fake_data = FakeData(session=session, num_records=5)
        await fake_data()


if __name__ == "__main__":
    asyncio.run(main())
