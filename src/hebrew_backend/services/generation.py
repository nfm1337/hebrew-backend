from pydantic import BaseModel

from hebrew_backend.models import Level
from hebrew_backend.services.llm import get_default_model, get_provider, parse_model_string

LEVEL_DESCRIPTIONS = {
    Level.A1: "очень простые предложения, только настоящее время, базовая лексика",
    Level.A2: "простые предложения, прошедшее время, редко будущее время, повседневные ситуации",
    Level.B1: "более сложные конструкции, разнообразные времена, тематическая лексика",
}

TARGET_WORD_COUNT = {
    Level.A1: 2,
    Level.A2: 4,
    Level.B1: 6,
}


class HebrewTextResult(BaseModel):
    generated_text: str
    target_words: list[str]
    translation: str


def _build_prompt(level: Level, topic: str) -> str:
    return f"""Создай короткий текст на иврите для русскоязычного студента.
Уровень: {level.value} — {LEVEL_DESCRIPTIONS[level]}
Тема: {topic}
Новых слов: {TARGET_WORD_COUNT[level]}
Требования: длина 50-100 слов, сложность строго {level.value}, текст связный.
Верни: generated_text (иврит), target_words (леммы новых слов), translation (русский)."""


async def generate_hebrew_session(
    level: Level, topic: str, model: str | None = None
) -> HebrewTextResult:
    chosen_model = model or get_default_model()
    provider = get_provider(chosen_model)
    _, model_name = parse_model_string(chosen_model)

    return await provider.generate_structured(
        model=model_name,
        prompt=_build_prompt(level, topic),
        response_model=HebrewTextResult,
        max_tokens=1000,
    )
