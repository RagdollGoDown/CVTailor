from fastapi import APIRouter

from app.llm import LLM

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(llm: LLM) -> dict:
    return {"status": "ok", "llm_provider": llm.name}
