from datetime import UTC, date, datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, DateTime, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel

from hebrew_backend.enums import Binyan, Gender, GrammaticalNumber, Level, PartOfSpeech, VocabStatus


def _enum_column(enum_class: type, nullable: bool = True) -> Column:
    return Column(SAEnum(enum_class, name=enum_class.__name__.lower()), nullable=nullable)


class User(SQLModel, table=True):
    __tablename__ = "app_user"  # pyright: ignore[reportAssignmentType]
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    level: Level = Field(sa_column=_enum_column(Level, nullable=False))
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
    level: Level = Field(sa_column=_enum_column(Level, nullable=False))
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
    status: VocabStatus = Field(sa_column=_enum_column(VocabStatus, nullable=False))
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


class WordAnalysisCache(SQLModel, table=True):
    __tablename__ = "word_analysis_cache"  # pyright: ignore[reportAssignmentType]
    __table_args__ = (UniqueConstraint("lemma", "pos", name="uq_word_analysis_lemma_pos"),)

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    word: str
    word_normalized: str
    lemma: str
    root: str | None = None
    binyan: Binyan | None = Field(default=None, sa_column=_enum_column(Binyan))
    pos: PartOfSpeech = Field(sa_column=_enum_column(PartOfSpeech, nullable=False))
    gender: Gender | None = Field(default=None, sa_column=_enum_column(Gender))
    number: GrammaticalNumber | None = Field(
        default=None, sa_column=_enum_column(GrammaticalNumber)
    )
    translation_ru: str
    related_words: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
