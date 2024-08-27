import os
import tempfile

import pytest
from httpx import AsyncClient
from tests.conftest import TEST_SECURITY_KEY


@pytest.mark.asyncio
async def test_send_image(ac: AsyncClient):
    headers = {"Api-key": TEST_SECURITY_KEY}

    # Создание временного файла изображения для тестирования
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(b"fake image data")  # Записываем фейковые данные изображения
        tmp_file_path = tmp_file.name  # Получаем путь к временно созданному файлу

    try:
        # Открываем временный файл для чтения в режиме бинарного файла
        with open(tmp_file_path, "rb") as f:
            response = await ac.post(
                "/api/medias",
                files={"file": f},
                headers=headers,
            )

        # Проверяем статус-код ответа и корректность полученных данных
        assert response.status_code == 200
        assert response.json() == {
            "result": True,
            "media_id": 1,  # Проверьте, что это значение соответствует ожидаемому
        }

    finally:
        # Удаляем временный файл после выполнения теста
        os.remove(tmp_file_path)
