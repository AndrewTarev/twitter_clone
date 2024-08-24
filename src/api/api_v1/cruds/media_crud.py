import os
import pathlib
import time

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import Media, User
from src.utils.logging_config import logger


async def handle_uploaded_file(file: UploadFile, session: AsyncSession, user: User):
    relative_directory = pathlib.Path(__file__).parent.parent.parent.parent.parent
    abs_path = f"{relative_directory}/static/images"
    logger.info(f"relative path: {relative_directory}")

    # создаем уникальное имя файла
    _, file_extension = file.content_type.split("/")
    timestamp: int = int(time.time() * 1000)
    new_file_name = f"{timestamp}_{user.id}.{file_extension}"
    file_location: str = os.path.join(abs_path, new_file_name)
    logger.info(f"Uploading {file_location}")

    media: Media = Media(link=file_location, file_name=new_file_name)

    async with aiofiles.open(file_location, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    session.add(media)
    await session.commit()
    logger.info(f"Создан медиа файл - {media}")

    return media.id
