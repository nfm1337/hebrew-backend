from evals.judges import JUDGE_MODEL, GrammarJudgement
from hebrew_backend.services.llm import get_provider, parse_model_string

JUDGE_PROMPT = """You are an expert in Hebrew linguistics, evaluating grammatical correctness of educational texts.

Read the following Hebrew text:

TEXT:
{text}

Your task:
1. Is the text grammatically correct overall?
2. List all grammatical errors found — for each provide:
   - The problematic phrase
   - What is wrong
   - The correct form
3. Overall severity: none / minor / major
4. Confidence score (0.0-1.0)
5. Brief justification

Be strict. Even minor errors (wrong gender agreement, incorrect verb conjugation, missing definite article) must be reported."""


async def judge_grammar(text: str) -> GrammarJudgement:
    _, model_name = parse_model_string(JUDGE_MODEL)
    return await get_provider(JUDGE_MODEL).generate_structured(
        model=model_name,
        prompt=JUDGE_PROMPT.format(text=text),
        response_model=GrammarJudgement,
    )
