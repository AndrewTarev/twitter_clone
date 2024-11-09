import os
import pathlib
import time

import aiofiles  # type: ignore
from backend.src.core import Media, User
from backend.src.utils.logging_config import my_logger
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


async def handle_uploaded_file(
    file: UploadFile, session: AsyncSession, user: User
) -> int:

    # Определяем директорию для сохранения
    relative_directory = (
        pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent.parent
        / "/usr/share/nginx/html/images/"
    )
    os.makedirs(
        relative_directory, exist_ok=True
    )  # Создаем директорию, если не существует

    # Создаем уникальное имя файла
    _, file_extension = file.content_type.split("/")  # type: ignore
    timestamp: int = int(time.time() * 1000)
    new_file_name = f"{timestamp}_{user.id}.{file_extension}"
    file_location: str = os.path.join(relative_directory, new_file_name)
    my_logger.info(f"file_location - {file_location}")

    nginx_path: str = os.path.join("/images/", new_file_name)
    my_logger.info(f"nginx_path - {nginx_path}")
    media: Media = Media(link=nginx_path, file_name=new_file_name)

    try:
        async with aiofiles.open(file_location, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        session.add(media)
        await session.commit()
        my_logger.info(f"Создан медиа файл - {media}")
    except Exception as e:
        my_logger.error(f"Ошибка при загрузке файла: {e}")
        raise

    return media.id
