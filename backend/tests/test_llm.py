import json

import httpx
import pytest

from app.llm.base import Message
from app.llm.dummy import CANNED_RESPONSES, DummyProvider
from app.llm.openai_compatible import OpenAICompatibleProvider
from app.llm.structured import complete_structured
from app.schemas import ExtractedItems

VALID = json.dumps(CANNED_RESPONSES["extract_items"])


def fake_api(answer: str, requests: list[dict]) -> httpx.Client:
    """An httpx client whose requests never leave the process. Records each request body."""

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(
            {"url": str(request.url), "auth": request.headers["Authorization"], **json.loads(request.content)}
        )
        return httpx.Response(
            200,
            json={
                "model": "qwen3",
                "choices": [{"message": {"role": "assistant", "content": answer}}],
                "usage": {"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150},
            },
        )

    return httpx.Client(transport=httpx.MockTransport(handler))


def provider(requests: list[dict], **kwargs) -> OpenAICompatibleProvider:
    return OpenAICompatibleProvider(
        "https://api.example.com/2/ai/1/openai/v1/", "secret", "qwen3", client=fake_api(VALID, requests), **kwargs
    )


def test_sends_schema_as_json_schema_response_format():
    requests: list[dict] = []
    llm = provider(requests, reasoning_effort="none", max_completion_tokens=500)

    result = complete_structured(llm, "extract_items", [Message("user", "hi")], ExtractedItems)

    sent = requests[0]
    assert sent["url"] == "https://api.example.com/2/ai/1/openai/v1/chat/completions"
    assert sent["auth"] == "Bearer secret"
    assert sent["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "extract_items", "schema": ExtractedItems.model_json_schema(), "strict": False},
    }
    assert sent["reasoning_effort"] == "none"
    assert sent["max_completion_tokens"] == 500
    assert result.usage.input_tokens == 120 and result.usage.output_tokens == 30


def test_schema_is_left_out_of_the_prompt_when_the_api_enforces_it():
    requests: list[dict] = []
    complete_structured(provider(requests), "extract_items", [Message("user", "hi")], ExtractedItems)
    assert "JSON schema" not in requests[0]["messages"][-1]["content"]


def test_without_structured_output_the_schema_goes_in_the_prompt():
    requests: list[dict] = []
    complete_structured(
        provider(requests, structured_output=False), "extract_items", [Message("user", "hi")], ExtractedItems
    )
    assert "response_format" not in requests[0]
    assert "JSON schema" in requests[0]["messages"][-1]["content"]


def test_optional_parameters_are_not_sent_when_unset():
    requests: list[dict] = []
    provider(requests).complete("extract_items", [Message("user", "hi")])
    assert not {"response_format", "reasoning_effort", "max_completion_tokens"} & requests[0].keys()


def test_missing_configuration_fails_early():
    with pytest.raises(ValueError):
        OpenAICompatibleProvider("", "", "")


def test_dummy_gets_the_schema_in_the_prompt():
    llm = DummyProvider()
    complete_structured(llm, "extract_items", [Message("user", "hi")], ExtractedItems)
    assert "JSON schema" in llm.calls_for("extract_items")[0][-1].content
