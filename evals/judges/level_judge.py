from evals.cache import cached_generate_structured
from evals.judges import JUDGE_MODEL, LevelJudgement

LEVEL_DESCRIPTIONS = """
A1: present tense only, basic vocabulary (1000 most frequent words), simple declarative sentences, no complex constructions
A2: adds past/future tense, basic modal verbs, simple subordinate clauses with כי/אם, everyday vocabulary (~2000 words)
B1: all main tenses, hif'il/hitpa'el binyanim, passive voice, thematic vocabulary (3000-4000 words), complex sentences
"""

JUDGE_PROMPT = """You are an expert in Hebrew pedagogy and linguistics, evaluating educational texts.

Read the following Hebrew text generated for a student at level {expected_level}:

TEXT:
{text}

DECLARED TARGET WORDS (new vocabulary for this level):
{target_words}

LEVELS:
{level_descriptions}

Your task:
1. Determine the actual level of the text (A1/A2/B1/B2/C1)
2. Does it match the declared level {expected_level}?
3. List problematic words — those that are ABOVE the declared level (excluding target_words, which are intentionally new vocabulary for this level)
4. Confidence score (0.0-1.0)
5. Brief justification

Be strict. If an A1 text contains past tense — it is no longer A1. If a B1 text uses only the simplest vocabulary — that is also a mismatch."""


async def judge_level(
    text: str,
    expected_level: str,
    target_words: list[str],
) -> LevelJudgement:
    return await cached_generate_structured(
        model=JUDGE_MODEL,
        prompt=JUDGE_PROMPT.format(
            text=text,
            expected_level=expected_level,
            target_words=", ".join(target_words),
            level_descriptions=LEVEL_DESCRIPTIONS,
        ),
        response_model=LevelJudgement,
    )
