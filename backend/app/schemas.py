"""API and LLM-output schemas. Mirrors docs/DataModels.md; extend as each phase is built."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

from app.llm.base import Usage

ItemType = Literal["job", "education", "course", "project", "extracurricular", "award", "recommendation", "other"]
PartialDate = Annotated[str, StringConstraints(pattern=r"^\d{4}(-(0[1-9]|1[0-2]))?$")]


class ExperienceItemDraft(BaseModel):
    """An experience item as extracted by the LLM, before the user reviews it. The browser adds id and timestamps."""

    type: ItemType
    title: str = Field(min_length=1)
    organization: str | None = None
    start_date: PartialDate | None = None
    end_date: PartialDate | Literal["present"] | None = None
    body: str
    skills: list[str] = []


class ExtractedItems(BaseModel):
    """LLM output for the extract_items task."""

    items: list[ExperienceItemDraft]


class ExtractItemsRequest(BaseModel):
    text: str = Field(min_length=1)
    type_hint: ItemType | None = None


class ExtractItemsResponse(BaseModel):
    items: list[ExperienceItemDraft]
    usage: Usage
