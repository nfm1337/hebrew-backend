from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMProvider(Protocol):
    """LLM-providers contract.

    All providers returns typed result via instructor.
    Business logic don't know about concrete provider.
    """

    provider_name: str

    async def generate_structured(
        self, model: str, prompt: str, response_model: type[T], max_tokens: int = 1000
    ) -> T:
        """Generate answer validated by response_model.

        Args:
            model: model name in provider notation (claude-sonnet-4-6-....)
            prompt: user message
            response_model: pydantic model for structured output
            max_tokens: token limit for answer

        Returns:
            response_model instance

        Raises:
            LLMProviderError: if provider not available or answer can't be parsed.
        """
        ...


class LLMProviderError(Exception):
    """Base provider error. Wraps SDK specific errors."""

    def __init__(self, provider: str, message: str, original: Exception | None = None) -> None:
        self.provider = provider
        self.original = original
        super().__init__(f"[{provider}] {message}")
