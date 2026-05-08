from contextlib import asynccontextmanager

from fastapi import FastAPI

from hebrew_backend.database import engine
from hebrew_backend.routers import health


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
