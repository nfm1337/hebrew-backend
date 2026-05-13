"""Local dedup cache for eval LLM calls.

Кеш срабатывает на точное совпадение (model, prompt, response_model schema, max_tokens).
Повторный прогон с теми же входами вообще не делает сетевых вызовов.

Инвалидация:
- Изменение текста промпта (JUDGE_PROMPT, _build_prompt) → ключ меняется.
- Изменение полей в Pydantic-моделях → JSON-schema меняется, ключ меняется.
- Вручную: ``rm -rf evals/.eval_cache``.

Хранится по одному JSON-файлу на запись, чтобы можно было грепать и удалять
конкретные записи.
"""

import hashlib
import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from hebrew_backend.models import Level
from hebrew_backend.services.generation import HebrewTextResult, _build_prompt
from hebrew_backend.services.llm import get_provider, parse_model_string

T = TypeVar("T", bound=BaseModel)

_CACHE_DIR = Path(__file__).parent / ".eval_cache"
_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _key_path(model: str, prompt: str, response_model: type[BaseModel], max_tokens: int) -> Path:
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "schema": response_model.model_json_schema(),
            "max_tokens": max_tokens,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return _CACHE_DIR / f"{digest}.json"


async def cached_generate_structured[T: BaseModel](
    model: str,
    prompt: str,
    response_model: type[T],
    max_tokens: int = 1000,
) -> T:
    """Cached drop-in для ``LLMProvider.generate_structured()``.

    На cache hit возвращает результат из локального JSON без сетевого вызова.
    На miss — обычный вызов через provider registry, затем атомарная запись на диск.
    """
    path = _key_path(model, prompt, response_model, max_tokens)
    if path.exists():
        return response_model.model_validate_json(path.read_text(encoding="utf-8"))

    _, model_name = parse_model_string(model)
    result = await get_provider(model).generate_structured(
        model=model_name,
        prompt=prompt,
        response_model=response_model,
        max_tokens=max_tokens,
    )

    tmp = path.with_suffix(".tmp")
    tmp.write_text(result.model_dump_json(), encoding="utf-8")
    tmp.replace(path)
    return result


async def cached_generate_hebrew_session(level: Level, topic: str, model: str) -> HebrewTextResult:
    """Cached версия ``generate_hebrew_session`` для использования в evals."""
    return await cached_generate_structured(
        model=model,
        prompt=_build_prompt(level, topic),
        response_model=HebrewTextResult,
        max_tokens=2000,
    )
