from fastapi import APIRouter, HTTPException

from app.config import settings
from app.llm import LLM
from app.llm.structured import StructuredOutputError, complete_structured
from app.prompts import extract_items
from app.schemas import ExtractedItems, ExtractItemsRequest, ExtractItemsResponse

router = APIRouter(prefix="/api/items", tags=["items"])


@router.post("/extract", response_model=ExtractItemsResponse)
def extract(request: ExtractItemsRequest, llm: LLM) -> ExtractItemsResponse:
    """Phase 1: turn pasted text into experience items. Nothing is stored (docs/Privacy.md)."""
    if len(request.text) > settings.max_input_chars:
        raise HTTPException(413, f"Text is too long (max {settings.max_input_chars} characters).")
    try:
        result = complete_structured(
            llm, "extract_items", extract_items.build_messages(request.text, request.type_hint), ExtractedItems
        )
    except StructuredOutputError:
        raise HTTPException(502, "The AI returned an unusable answer. Please try again.") from None
    return ExtractItemsResponse(items=result.value.items, usage=result.usage)
