# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from .routers import router as api_router
from settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await Tortoise.init(
        db_url=settings.database.url,
        modules={"models": ["application.models"]},
    )
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")
app.mount(
    "/",
    StaticFiles(directory=settings.frontend.dist_path, html=True, check_dir=False),
    name="static",
)
