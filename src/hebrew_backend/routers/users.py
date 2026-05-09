from fastapi import APIRouter

from hebrew_backend.database import SessionDep
from hebrew_backend.models import User
from hebrew_backend.schemas import CreateUserRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(request: CreateUserRequest, session: SessionDep) -> User:
    user = User(level=request.level, topics=request.topics)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
