from typing import AsyncGenerator

import pytest_asyncio
from backend.src.core.base import Base
from backend.src.core.config import TestingConfig
from backend.src.core.db_helper import db_helper
from backend.src.main import app
from backend.src.utils.faker_db import FakeData
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

testing_conf = TestingConfig()
TEST_NAME = "test"
TEST_SECURITY_KEY = "test"
DATABASE_URL = testing_conf.url

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


app.dependency_overrides[db_helper.session_getter] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        faker_data = FakeData(session=session, num_records=5)
        await faker_data()
        yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"  # type: ignore
    ) as async_client:
        yield async_client
