import json

from app.llm.base import LLMResponse, Message, Usage

CANNED_RESPONSES: dict[str, dict] = {
    "extract_items": {
        "items": [
            {
                "type": "course",
                "title": "Machine Learning",
                "organization": "Example University",
                "start_date": "2024-09",
                "end_date": "2025-01",
                "body": "Supervised and unsupervised learning, model evaluation, and a group project on text classification.",
                "skills": ["Python", "scikit-learn", "Machine learning"],
            }
        ]
    },
}


class DummyProvider:
    """Returns canned answers per task. No network, no cost: for development and tests.

    `responses` overrides the canned answers. A list of strings is returned in order (the last one repeats),
    which lets tests simulate a bad answer followed by a good one.
    """

    name = "dummy"
    enforces_schema = False

    def __init__(self, responses: dict[str, str | list[str]] | None = None):
        self.responses = responses or {task: json.dumps(body) for task, body in CANNED_RESPONSES.items()}
        self.calls: list[tuple[str, list[Message]]] = []

    def complete(self, task: str, messages: list[Message], *, response_schema: dict | None = None) -> LLMResponse:
        if task not in self.responses:
            raise KeyError(f"No dummy response for task {task!r}")
        answer = self.responses[task]
        if isinstance(answer, list):
            text = answer[min(len(self.calls_for(task)), len(answer) - 1)]
        else:
            text = answer
        self.calls.append((task, messages))
        # Rough token estimate (~4 characters per token) so the cost display has something to show.
        input_chars = sum(len(m.content) for m in messages)
        return LLMResponse(
            text=text, model="dummy", usage=Usage(input_tokens=input_chars // 4, output_tokens=len(text) // 4)
        )

    def calls_for(self, task: str) -> list[list[Message]]:
        return [messages for t, messages in self.calls if t == task]
