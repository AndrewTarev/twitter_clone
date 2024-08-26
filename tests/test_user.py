# python -m pytest -v
import pytest
from httpx import AsyncClient
from tests.conftest import TEST_NAME, TEST_SECURITY_KEY


@pytest.mark.asyncio
async def test_get_current_user(ac: AsyncClient):

    headers = {"Api-key": TEST_SECURITY_KEY}

    response = await ac.get("/api/users/me", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True
    assert data["user"]["name"] == TEST_NAME


@pytest.mark.asyncio
async def test_get_current_user_invalid_api_key(ac: AsyncClient):
    headers = {"Api-key": "wrong_secret_key"}
    response = await ac.get("/api/users/me", headers=headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/api/users/1")
    data = response.json()
    assert response.status_code == 200
    assert data["result"] is True
    assert data["user"]["name"] == TEST_NAME


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(ac: AsyncClient):
    response = await ac.get("/api/users/10")
    data = response.json()
    assert response.status_code == 404
    assert data["result"] is False
