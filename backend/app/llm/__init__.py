from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.config import settings
from app.llm.base import LLMProvider, LLMResponse, Message, Usage
from app.llm.dummy import DummyProvider
from app.llm.openai_compatible import OpenAICompatibleProvider

__all__ = ["LLM", "LLMProvider", "LLMResponse", "Message", "Usage", "get_llm"]


@lru_cache
def get_llm() -> LLMProvider:
    """FastAPI dependency. Tests override it with `app.dependency_overrides`."""
    if settings.llm_provider == "openai_compatible":
        return OpenAICompatibleProvider(
            settings.llm_base_url, settings.llm_api_key, settings.llm_model, json_mode=settings.llm_json_mode
        )
    return DummyProvider()


LLM = Annotated[LLMProvider, Depends(get_llm)]
