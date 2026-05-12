import pytest
from pydantic import BaseModel

from hebrew_backend.services.llm import get_provider


class _Ping(BaseModel):
    answer: str


@pytest.mark.smoke
@pytest.mark.parametrize(
    "model",
    [
        "anthropic/claude-haiku-4-5",
        "google/gemini-2.5-flash",
    ],
)
async def test_provider_smoke(model: str) -> None:
    provider_name, model_name = model.split("/", 1)
    provider = get_provider(model)
    result = await provider.generate_structured(
        model=model_name,
        prompt='Reply with answer="ok"',
        response_model=_Ping,
        max_tokens=50,
    )
    assert result.answer
