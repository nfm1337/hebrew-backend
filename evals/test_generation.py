import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from evals.judges.grammar_judge import judge_grammar
from evals.judges.level_judge import judge_level
from evals.judges.topic_judge import judge_topic
from hebrew_backend.models import Level
from hebrew_backend.services.generation import generate_hebrew_session

MODELS_TO_TEST = [
    "anthropic/claude-sonnet-4-6",
    "openrouter/google/gemini-3-flash-preview",
    "openrouter/google/gemma-4-31b-it",
]


@pytest.mark.eval
@pytest.mark.parametrize("model", MODELS_TO_TEST)
async def test_generation_quality(case: dict[str, Any], model: str, report_dir: Path) -> None:
    level = Level[case["level"]]
    topic = case["topic"]

    result = await generate_hebrew_session(level=level, topic=topic, model=model)

    level_judgement, topic_judgement, grammar_judgement = await asyncio.gather(
        judge_level(result.generated_text, case["level"], result.target_words),
        judge_topic(result.generated_text, topic),
        judge_grammar(result.generated_text),
    )

    report = {
        "case_id": case["id"],
        "model": model,
        "timestamp": datetime.now(UTC).isoformat(),
        "input": {"level": case["level"], "topic": topic},
        "output": {
            "text": result.generated_text,
            "target_words": result.target_words,
            "translation": result.translation,
        },
        "judgements": {
            "level": level_judgement.model_dump(),
            "topic": topic_judgement.model_dump(),
            "grammar": grammar_judgement.model_dump(),
        },
    }

    report_file = report_dir / f"{case['id']}__{model.replace('/', '_')}.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2))

    failures = []
    if not level_judgement.matches_expected:
        failures.append(
            f"Level mismatch: expected {case['level']}, got {level_judgement.actual_level} "
            f"(problematic words: {level_judgement.problematic_words})"
        )
    if not topic_judgement.on_topic:
        failures.append(f"Off-topic: {topic_judgement.reasoning}")
    if grammar_judgement.severity == "major":
        failures.append(f"Major grammar issues: {grammar_judgement.errors}")

    if failures:
        pytest.fail("\n".join(failures))
