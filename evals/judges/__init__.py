from typing import Literal

from pydantic import BaseModel, Field

JUDGE_MODEL = "openrouter/google/gemini-3-flash-preview"


class LevelJudgement(BaseModel):
    actual_level: Literal["A1", "A2", "B1", "B2", "C1"]
    matches_expected: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    problematic_words: list[str] = Field(
        default_factory=list, description="Words that are higher than stated level"
    )


class TopicJudgement(BaseModel):
    on_topic: bool
    actual_topic: str
    off_topic_fragments: list[str] = Field(default_factory=list)
    relevance_score: float = Field(ge=0.0, le=1.0)
    reasoning: str


class GrammarError(BaseModel):
    phrase: str
    issue: str
    correction: str


class GrammarJudgement(BaseModel):
    is_grammatical: bool
    errors: list[GrammarError] = Field(default_factory=list)
    severity: Literal["none", "minor", "major"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
