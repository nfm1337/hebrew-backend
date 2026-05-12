from typing import TypeVar, cast

import instructor
from anthropic import AsyncAnthropic
from google import genai
from openai import AsyncOpenAI
from pydantic import BaseModel

from hebrew_backend.services.llm.base import LLMProviderError

T = TypeVar("T", bound=BaseModel)


class AnthropicProvider:
    provider_name = "anthropic"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("Anthropic key is required")
        self._client = instructor.from_anthropic(AsyncAnthropic(api_key=api_key))

    async def generate_structured(
        self, model: str, prompt: str, response_model: type[T], max_tokens: int = 1000
    ) -> T:
        try:
            result = await self._client.messages.create(
                model=model,
                max_tokens=max_tokens,
                response_model=response_model,
                messages=[{"role": "user", "content": prompt}],
            )
            return cast("T", result)
        except Exception as e:
            raise LLMProviderError(self.provider_name, str(e), e) from e


class OpenAIProvider:
    provider_name = "openai"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self._client = instructor.from_openai(AsyncOpenAI(api_key=api_key))

    async def generate_structured(
        self,
        model: str,
        prompt: str,
        response_model: type[T],
        max_tokens: int = 1000,
    ) -> T:
        try:
            result = await self._client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return cast("T", result)
        except Exception as e:
            raise LLMProviderError(self.provider_name, str(e), e) from e


class GoogleProvider:
    provider_name = "google"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("Google API key is required")
        self._client = instructor.from_genai(
            genai.Client(api_key=api_key),
            mode=instructor.Mode.GENAI_TOOLS,
        )

    async def generate_structured(
        self,
        model: str,
        prompt: str,
        response_model: type[T],
        max_tokens: int = 1000,
    ) -> T:
        try:
            result = await self._client.chat.completions.create(
                model=model,
                response_model=response_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return cast("T", result)
        except Exception as e:
            raise LLMProviderError(self.provider_name, str(e), e) from e
