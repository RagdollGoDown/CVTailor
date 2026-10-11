import json
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError

from app.llm.base import LLMProvider, Message, Usage


class StructuredOutputError(Exception):
    """The LLM did not return valid JSON for the expected schema, even after retrying."""


@dataclass
class StructuredResult[T: BaseModel]:
    value: T
    usage: Usage  # summed over all attempts: the user pays for retries too


def complete_structured[T: BaseModel](
    llm: LLMProvider,
    task: str,
    messages: list[Message],
    response_model: type[T],
    max_attempts: int = 2,
) -> StructuredResult[T]:
    """Ask for JSON matching `response_model`, validate it, and retry with the error message if it doesn't match.

    Works whether or not the provider has a JSON mode: the schema is always put in the prompt and the answer
    is always validated (docs/Security.md S1).
    """
    schema = json.dumps(response_model.model_json_schema())
    instructions = Message(
        "system",
        "Respond with a single JSON object and nothing else (no prose, no code fences). "
        f"It must match this JSON schema:\n{schema}",
    )
    conversation = [*messages, instructions]
    usage = Usage()
    last_error = ""

    for _ in range(max_attempts):
        response = llm.complete(task, conversation, json_output=True)
        usage += response.usage
        try:
            return StructuredResult(response_model.model_validate_json(_extract_json(response.text)), usage)
        except (ValidationError, ValueError) as e:
            last_error = str(e)
            conversation = [
                *conversation,
                Message("assistant", response.text),
                Message(
                    "user",
                    f"Your answer was not valid. Error:\n{last_error}\nReply again with only the corrected JSON.",
                ),
            ]

    raise StructuredOutputError(f"{task}: no valid answer after {max_attempts} attempts. Last error: {last_error}")


def _extract_json(text: str) -> str:
    """Tolerate the usual wrapping (code fences, a sentence before or after) by taking the outermost object."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end < start:
        raise ValueError("No JSON object found in the answer")
    return text[start : end + 1]
