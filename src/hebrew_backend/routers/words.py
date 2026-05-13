from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from hebrew_backend.database import SessionDep
from hebrew_backend.models import WordAnalysisCache
from hebrew_backend.schemas import WordAnalysis, WordAnalysisRequest, WordAnalysisResponse
from hebrew_backend.services.word_analysis import (
    generate_word_analysis,
    get_cached_analysis,
    strip_nikud,
)

router = APIRouter(prefix="/words", tags=["words"])


@router.post("/analysis", response_model=WordAnalysisResponse)
async def word_analysis(request: WordAnalysisRequest, db: SessionDep) -> WordAnalysisResponse:
    normalized = strip_nikud(request.word)
    cache_hit = await get_cached_analysis(normalized, db)
    if cache_hit:
        return WordAnalysisResponse(
            analysis=_model_to_schema(cache_hit),
            cached=True,
        )
    result = await generate_word_analysis(
        word=request.word, sentence=request.sentence, model=request.model
    )
    cache_entry = _schema_to_model(schema=result, normalized_word=normalized)
    try:
        db.add(cache_entry)
        await db.commit()
    except IntegrityError:
        await db.rollback()

    return WordAnalysisResponse(
        analysis=result,
        cached=False,
    )


def _model_to_schema(model: WordAnalysisCache) -> WordAnalysis:
    return WordAnalysis(
        word=model.word,
        lemma=model.lemma,
        root=model.root,
        binyan=model.binyan,
        pos=model.pos,
        gender=model.gender,
        number=model.number,
        translation_ru=model.translation_ru,
        related_words=model.related_words,
    )


def _schema_to_model(schema: WordAnalysis, normalized_word: str) -> WordAnalysisCache:
    return WordAnalysisCache(
        word=schema.word,
        word_normalized=normalized_word,
        lemma=schema.lemma,
        root=schema.root,
        binyan=schema.binyan,
        pos=schema.pos,
        gender=schema.gender,
        number=schema.number,
        translation_ru=schema.translation_ru,
        related_words=schema.related_words,
    )
