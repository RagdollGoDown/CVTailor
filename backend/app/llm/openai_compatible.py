from dataclasses import asdict

import httpx

from app.llm.base import LLMResponse, Message, Usage


class OpenAICompatibleProvider:
    """Any API that speaks the OpenAI chat-completions format (the target is Infomaniak AI)."""

    name = "openai_compatible"

    def __init__(self, base_url: str, api_key: str, model: str, json_mode: bool = False, timeout: float = 120.0):
        if not (base_url and api_key and model):
            raise ValueError("LLM_BASE_URL, LLM_API_KEY and LLM_MODEL must be set for the openai_compatible provider")
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.api_key = api_key
        self.model = model
        self.json_mode = json_mode
        self.timeout = timeout

    def complete(self, task: str, messages: list[Message], *, json_output: bool = False) -> LLMResponse:
        payload: dict = {"model": self.model, "messages": [asdict(m) for m in messages]}
        if json_output and self.json_mode:
            payload["response_format"] = {"type": "json_object"}
        response = httpx.post(
            self.url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        usage = data.get("usage") or {}
        return LLMResponse(
            text=data["choices"][0]["message"]["content"],
            model=data.get("model", self.model),
            usage=Usage(input_tokens=usage.get("prompt_tokens", 0), output_tokens=usage.get("completion_tokens", 0)),
        )
