from typing import AsyncGenerator

import pytest_asyncio
from backend.src.core import Base, SecurityKey, User
from backend.src.core.config import settings
from backend.src.core.db_helper import db_helper
from backend.src.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_NAME = "test_name"
TEST_SECURITY_KEY = "test_security_key"
DATABASE_URL = settings.test_db.url

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


app.dependency_overrides[db_helper.session_getter] = override_get_db


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def create_user(db_session: AsyncSession):
    user = User(name=TEST_NAME)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    security_key = SecurityKey(user_id=user.id, key=TEST_SECURITY_KEY)
    db_session.add(security_key)
    await db_session.commit()

    return user, security_key.key
