from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

from backend.src.api.api_v1.routers import router
from backend.src.core.db_helper import db_helper
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await db_helper.dispose()


app = FastAPI()


instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.status_code,
            "error_message": exc.detail,
        },
    )


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
