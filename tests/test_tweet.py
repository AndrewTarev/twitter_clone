import pytest
from httpx import AsyncClient
from tests.conftest import TEST_SECURITY_KEY

TWEET_ID: int = 0


@pytest.mark.asyncio
async def test_add_tweet(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.post(
        "/api/tweets",
        headers=headers,
        json={
            "tweet_data": "test_tweet_data",
        },
    )
    data = response.json()
    global TWEET_ID
    TWEET_ID = data["tweet_id"]
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_all_tweets(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.get(
        "/api/tweets",
        headers=headers,
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"] is True


@pytest.mark.asyncio
async def test_delete_your_tweet(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.delete(
        f"/api/tweets/{TWEET_ID}",
        headers=headers,
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_not_your_tweet(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.delete(
        "/api/tweets/1",
        headers=headers,
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_like_tweet(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.post(
        "/api/tweets/2/likes",
        headers=headers,
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_like_non_existent_tweet(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.post(
        "/api/tweets/999/likes",
        headers=headers,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_unlike_tweet(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}
    response = await ac.delete(
        "/api/tweets/2/likes",
        headers=headers,
    )
    assert response.status_code == 204
