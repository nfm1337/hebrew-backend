from uuid import UUID

from openai import BaseModel

from hebrew_backend.models import Level


class GenerateSessionRequest(BaseModel):
    user_id: UUID
    level: Level
    topic: str


class GenerateSessionResponse(BaseModel):
    session_id: UUID
    generated_text: str
    target_words: list[str]
    translation: str
