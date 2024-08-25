from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from backend.src.api.api_v1.routers import router
from backend.src.core.db_helper import db_helper
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await db_helper.dispose()


app = FastAPI()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
