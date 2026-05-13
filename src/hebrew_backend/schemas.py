from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from hebrew_backend.enums import Binyan, Gender, GrammaticalNumber, Level, PartOfSpeech


class GenerateSessionRequest(BaseModel):
    user_id: UUID
    level: Level
    topic: str
    model: str | None = None


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


class WordAnalysisRequest(BaseModel):
    word: str
    sentence: str
    model: str | None = None


class WordAnalysis(BaseModel):
    model_config = {"from_attributes": True}

    word: str
    lemma: str
    root: str | None
    binyan: Binyan | None
    pos: PartOfSpeech
    gender: Gender | None
    number: GrammaticalNumber | None
    translation_ru: str
    related_words: list[str]


class WordAnalysisResponse(BaseModel):
    analysis: WordAnalysis
    cached: bool
