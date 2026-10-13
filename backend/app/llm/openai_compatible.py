from dataclasses import asdict
from typing import Literal

import httpx

from app.llm.base import LLMResponse, Message, Usage

ReasoningEffort = Literal["none", "low", "medium", "high"]


class OpenAICompatibleProvider:
    """Any API that speaks the OpenAI chat-completions format. The target is Infomaniak AI:
    https://developer.infomaniak.com/docs/api/post/2/ai/%7Bproduct_id%7D/openai/v1/chat/completions
    """

    name = "openai_compatible"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        *,
        structured_output: bool = True,
        strict_schema: bool = False,
        reasoning_effort: ReasoningEffort | None = None,
        max_completion_tokens: int | None = None,
        client: httpx.Client | None = None,
    ):
        if not (base_url and api_key and model):
            raise ValueError("LLM_BASE_URL, LLM_API_KEY and LLM_MODEL must be set for the openai_compatible provider")
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.api_key = api_key
        self.model = model
        self.enforces_schema = structured_output
        self.strict_schema = strict_schema
        self.reasoning_effort = reasoning_effort
        self.max_completion_tokens = max_completion_tokens
        self.client = client or httpx.Client(timeout=120.0)

    def complete(self, task: str, messages: list[Message], *, response_schema: dict | None = None) -> LLMResponse:
        payload: dict = {"model": self.model, "messages": [asdict(m) for m in messages]}
        if response_schema is not None and self.enforces_schema:
            # Infomaniak only supports "json_schema" ("json_object" is no longer supported).
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": task, "schema": response_schema, "strict": self.strict_schema},
            }
        if self.reasoning_effort is not None:
            payload["reasoning_effort"] = self.reasoning_effort
        if self.max_completion_tokens is not None:
            payload["max_completion_tokens"] = self.max_completion_tokens

        response = self.client.post(self.url, headers={"Authorization": f"Bearer {self.api_key}"}, json=payload)
        response.raise_for_status()
        data = response.json()
        usage = data.get("usage") or {}
        return LLMResponse(
            text=data["choices"][0]["message"]["content"],
            model=data.get("model", self.model),
            usage=Usage(input_tokens=usage.get("prompt_tokens", 0), output_tokens=usage.get("completion_tokens", 0)),
        )
