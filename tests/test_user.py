# python -m pytest -v
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user(ac: AsyncClient, create_user):
    user, api_key = create_user

    # Устанавливаем заголовок API ключа
    headers = {"Api-key": api_key}

    response = await ac.get("/api/users/me", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True
    assert data["user"]["name"] == user.name
