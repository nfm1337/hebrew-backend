import instructor
from anthropic import AsyncAnthropic
from openai import BaseModel

from hebrew_backend.models import Level
from hebrew_backend.settings import settings

client = instructor.from_anthropic(AsyncAnthropic(api_key=settings.anthropic_api_key))

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


async def generate_hebrew_session(level: Level, topic: str) -> HebrewTextResult:
    result: HebrewTextResult = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        response_model=HebrewTextResult,
        messages=[
            {
                "role": "user",
                "content": f"""Создай короткий текст на иврите для русскоязычного студента.

Уровень: {level.value} — {LEVEL_DESCRIPTIONS[level]}
Тема: {topic}
Новых слов: {TARGET_WORD_COUNT[level]}

Требования:
- Длина 50-100 слов
- Сложность строго соответствует уровню {level.value}
- Текст связный и естественный
- Новые слова вводятся органично в контекст

Верни:
- generated_text: текст на иврите
- target_words: список новых слов в базовой форме (инфинитив для глаголов, единственное число для существительных)
- translation: полный перевод на русский язык""",
            }
        ],
    )
    return result
