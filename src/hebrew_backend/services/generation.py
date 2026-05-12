from pydantic import BaseModel

from hebrew_backend.models import Level
from hebrew_backend.services.llm import get_default_model, get_provider, parse_model_string

LEVEL_DESCRIPTIONS = {
    Level.A1: "present tense only, ~1000 most frequent words, simple declarative sentences, no subordinate clauses",
    Level.A2: "past and future tense, basic modal verbs, simple subordinate clauses with כי/אם, ~2000 words",
    Level.B1: "all main tenses, hif'il/hitpa'el binyanim, passive voice, thematic vocabulary ~3000-4000 words, complex sentences",
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
    return f"""Write a short Hebrew text for a Russian-speaking student learning Hebrew.

Level: {level.value} — {LEVEL_DESCRIPTIONS[level]}
Topic: {topic}
New vocabulary words to introduce: {TARGET_WORD_COUNT[level]}

Requirements:
- Length: 50-100 words
- Complexity MUST strictly match level {level.value} — do not use grammar or vocabulary above this level
- "{topic}" is the CENTRAL subject of the text. Every sentence must be about {topic}. Do NOT drift into generic descriptions or unrelated daily life scenes.
- Do NOT write about "learning Hebrew", "studying words", or language learning itself
- The new words must appear naturally in context

Return:
- generated_text: the Hebrew text
- target_words: list of new words in base form (infinitive for verbs, singular for nouns)
- translation: full Russian translation of the text"""


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
