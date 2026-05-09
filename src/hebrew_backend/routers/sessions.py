from uuid import uuid4

from fastapi import APIRouter

from hebrew_backend.database import SessionDep
from hebrew_backend.models import LearningSession
from hebrew_backend.schemas import GenerateSessionRequest, GenerateSessionResponse
from hebrew_backend.services.generation import generate_hebrew_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/generate", response_model=GenerateSessionResponse)
async def generate_session(
    request: GenerateSessionRequest, db: SessionDep
) -> GenerateSessionResponse:
    result = await generate_hebrew_session(request.level, request.topic)

    session = LearningSession(
        id=uuid4(),
        user_id=request.user_id,
        topic=request.topic,
        level=request.level,
        generated_text=result.generated_text,
        target_words=result.target_words,
    )
    db.add(session)
    await db.commit()

    return GenerateSessionResponse(
        session_id=session.id,
        generated_text=result.generated_text,
        target_words=result.target_words,
        translation=result.translation,
    )
