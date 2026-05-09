from datetime import UTC, date, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, SQLModel


class Level(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"


class VocabStatus(StrEnum):
    LEARNING = "learning"
    KNOWN = "known"
    MASTERED = "mastered"


class User(SQLModel, table=True):
    __tablename__ = "app_user"  # pyright: ignore[reportAssignmentType]
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    level: Level
    topics: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class LearningSession(SQLModel, table=True):
    __tablename__ = "learning_session"  # pyright: ignore[reportAssignmentType]
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(foreign_key="app_user.id")
    topic: str
    level: Level
    generated_text: str
    target_words: list[str] = Field(sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class UserVocabulary(SQLModel, table=True):
    __tablename__ = "user_vocabulary"  # pyright: ignore[reportAssignmentType]
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(foreign_key="app_user.id")
    lemma: str
    status: VocabStatus
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True), nullable=False, onupdate=lambda: datetime.now(UTC)
        ),
    )


class Card(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_vocab_id: UUID = Field(foreign_key="user_vocabulary.id")
    ease_factor: float = 2.5
    interval_days: int = 1
    due_date: date
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    last_review_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    review_count: int = 0


class CardReview(SQLModel, table=True):
    __tablename__ = "card_review"  # pyright: ignore[reportAssignmentType]
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    card_id: UUID = Field(foreign_key="card.id")
    rating: int
    example_sentence: str
    reviewed_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))


class WordAnalysis(SQLModel, table=True):
    __tablename__ = "word_analysis"  # pyright: ignore[reportAssignmentType]
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    word: str
    context_hash: str
    lemma: str
    root: str | None = None
    binyan: str | None = None
    translation: str
    related_words: list[str] = Field(sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
