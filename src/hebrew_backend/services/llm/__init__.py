from functools import lru_cache

from hebrew_backend.services.llm.base import LLMProvider, LLMProviderError
from hebrew_backend.services.llm.providers import AnthropicProvider, GoogleProvider, OpenAIProvider
from hebrew_backend.settings import settings

__all__ = [
    "LLMProvider",
    "LLMProviderError",
    "get_default_model",
    "get_provider",
    "parse_model_string",
]

_DEFAULT_MODELS_BY_PRIORITY = [
    ("anthropic", "claude-sonnet-4-6"),
    ("google", "gemini-2.5-pro"),
    ("openai", "gpt-4o"),
]


def parse_model_string(model: str) -> tuple[str, str]:
    if "/" not in model:
        raise ValueError(
            f"Model must be in 'provider/name' format, got: {model!r}. "
            f"Examples: 'anthropic/claude-sonnet-4-6', 'google/gemini-2.5-pro'"
        )
    provider, name = model.split("/", 1)
    return provider, name


@lru_cache(maxsize=1)
def _build_registry() -> dict[str, LLMProvider]:
    registry: dict[str, LLMProvider] = {}
    if settings.anthropic_api_key:
        registry["anthropic"] = AnthropicProvider(settings.anthropic_api_key)
    if settings.google_api_key:
        registry["google"] = GoogleProvider(settings.google_api_key)
    if settings.openai_api_key:
        registry["openai"] = OpenAIProvider(settings.openai_api_key)
    return registry


def get_default_model() -> str:
    registry = _build_registry()
    for provider_name, model_name in _DEFAULT_MODELS_BY_PRIORITY:
        if provider_name in registry:
            return f"{provider_name}/{model_name}"

    raise RuntimeError("No default model available")


def get_provider(model: str) -> LLMProvider:
    """Получить провайдер по полному имени модели.

    Args:
        model: 'anthropic/claude-sonnet-4-6' или подобное.

    Raises:
        ValueError: некорректный формат или провайдер не сконфигурирован.
    """
    provider_name, _ = parse_model_string(model)
    registry = _build_registry()
    if provider_name not in registry:
        available = sorted(registry.keys())
        raise ValueError(
            f"Provider {provider_name!r} not configured. "
            f"Available: {available}. "
            f"Set {provider_name.upper()}_API_KEY in environment to enable."
        )
    return registry[provider_name]
