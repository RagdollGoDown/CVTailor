from dataclasses import dataclass
from typing import Literal, Protocol

from pydantic import BaseModel


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: str


class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
        )


@dataclass
class LLMResponse:
    text: str
    model: str
    usage: Usage


class LLMProvider(Protocol):
    """Interface every LLM backend implements. Prompts and parsing live elsewhere, so providers stay simple."""

    name: str

    def complete(self, task: str, messages: list[Message], *, json_output: bool = False) -> LLMResponse:
        """`task` names the pipeline step (e.g. "extract_items"). Used for usage tracking and by the dummy."""
        ...
