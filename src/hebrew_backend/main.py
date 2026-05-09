from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from hebrew_backend.database import engine
from hebrew_backend.routers import health, sessions, users


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(users.router)
