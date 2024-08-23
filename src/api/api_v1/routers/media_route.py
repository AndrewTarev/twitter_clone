from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.cruds.media_crud import handle_uploaded_file
from src.api.dependencies.user import get_user_dependency
from src.core import User
from src.core.config import settings
from src.core.db_helper import db_helper
from src.core.schemas.media_schemas import MediaOut
from src.utils.logging_config import logger

router = APIRouter(
    prefix=settings.api.medias,
    tags=["Media"],
)


@router.post("", response_model=MediaOut)
async def upload_media(
    files: UploadFile,
    user: User = Depends(get_user_dependency),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if not files.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File type not supported")

    media_id = await handle_uploaded_file(files=files, session=session, user=user)

    return {"result": True, "media_id": media_id}
