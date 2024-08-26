import os
import pathlib
import time

import aiofiles
from backend.src.core import Media, User
from backend.src.utils.logging_config import logger
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


async def handle_uploaded_file(file: UploadFile, session: AsyncSession, user: User):
    # Определяем директорию для сохранения
    relative_directory = (
        pathlib.Path(__file__).resolve().parent.parent.parent.parent.parent.parent
        / "frontend/static/images"
    )
    os.makedirs(
        relative_directory, exist_ok=True
    )  # Создаем директорию, если не существует

    logger.info(f"relative path: {relative_directory}")

    # Создаем уникальное имя файла
    _, file_extension = file.content_type.split("/")
    timestamp: int = int(time.time() * 1000)
    new_file_name = f"{timestamp}_{user.id}.{file_extension}"
    file_location: str = os.path.join(relative_directory, new_file_name)

    logger.info(f"Uploading {file_location}")

    media: Media = Media(link=file_location, file_name=new_file_name)

    try:
        async with aiofiles.open(file_location, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        session.add(media)
        await session.commit()
        logger.info(f"Создан медиа файл - {media}")
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}")
        raise

    return media.id
