import unicodedata

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from hebrew_backend.models import WordAnalysisCache
from hebrew_backend.schemas import WordAnalysis
from hebrew_backend.services.llm import get_default_model, get_provider, parse_model_string

PROMPT_TEMPLATE = """Analyze the following Hebrew word as it appears in context.

Word: {word}
Sentence: {sentence}

Requirements:
- word: the word exactly as given
- lemma: dictionary form (infinitive for verbs, masculine singular for nouns/adjectives), without nikud
- root: three or four letter root (e.g. כ-ת-ב), None for loanwords and particles
- binyan: one of: פעל, פיעל, הפעיל, התפעל, נפעל, פועל, הופעל — without nikud. None for non-verbs.
- pos: part of speech — verb, noun, adjective, adverb, preposition, pronoun, or other
- gender: masculine or feminine, None only for indeclinable words (adverbs, prepositions, conjunctions)
- number: singular, plural, or dual, None only for indeclinable words
- translation_ru: contextual Russian translation based on the sentence, not a generic dictionary entry
- related_words: 2-3 words sharing the same root, in base form, without nikud. Empty list for loanwords.

Return the analysis in the requested format."""


async def generate_word_analysis(
    word: str, sentence: str, model: str | None = None
) -> WordAnalysis:
    chosen_model = model or get_default_model()
    provider = get_provider(chosen_model)
    _, model_name = parse_model_string(chosen_model)

    return await provider.generate_structured(
        model=model_name,
        prompt=PROMPT_TEMPLATE.format(word=word, sentence=sentence),
        response_model=WordAnalysis,
        max_tokens=2000,
    )


async def get_cached_analysis(normalized_word: str, db: AsyncSession) -> WordAnalysisCache | None:
    result = await db.execute(
        select(WordAnalysisCache).where(WordAnalysisCache.word_normalized == normalized_word)
    )
    return result.scalar_one_or_none()


def strip_nikud(text: str) -> str:
    return "".join(c for c in text if unicodedata.category(c) != "Mn")
