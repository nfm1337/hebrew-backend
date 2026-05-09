from datetime import datetime
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


class CreateUserRequest(BaseModel):
    level: Level
    topics: list[str] = []


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    level: Level
    topics: list[str]
    created_at: datetime
