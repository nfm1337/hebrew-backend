from evals.judges import JUDGE_MODEL, TopicJudgement
from hebrew_backend.services.llm import get_provider, parse_model_string

JUDGE_PROMPT = """You are an expert in Hebrew pedagogy, evaluating whether an educational text stays on topic.

Read the following Hebrew text:

TEXT:
{text}

DECLARED TOPIC: {topic}

Your task:
1. Does the text genuinely focus on the declared topic, or does it merely mention it in passing?
2. What is the actual dominant topic of the text? (single short phrase)
3. List specific sentences or phrases that deviate from the declared topic
4. Relevance score (0.0-1.0) — how well the text matches the declared topic
5. Brief justification

Be strict. A text about "buying groceries" that spends most of its content describing a family's daily routine is OFF-TOPIC, even if a supermarket is mentioned. The declared topic must be the central subject, not a backdrop."""


async def judge_topic(text: str, expected_topic: str) -> TopicJudgement:
    _, model_name = parse_model_string(JUDGE_MODEL)
    return await get_provider(JUDGE_MODEL).generate_structured(
        model=model_name,
        prompt=JUDGE_PROMPT.format(text=text, topic=expected_topic),
        response_model=TopicJudgement,
    )
