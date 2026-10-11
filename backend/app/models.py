"""Server-side tables. Only non-personal data lives here (docs/Privacy.md)."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, BigInteger, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class CourseCacheEntry(Base):
    __tablename__ = "course_cache"

    # sha256(normalized text) + ":" + extraction prompt version
    key: Mapped[str] = mapped_column(String(96), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    institution: Mapped[str | None] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    skills: Mapped[list[str]] = mapped_column(JSON)
    hit_count: Mapped[int] = mapped_column(default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class UsageRecord(Base):
    """Token counts per LLM call, with no content. Feeds the cost display and the daily budget cap."""

    __tablename__ = "usage_records"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    task: Mapped[str] = mapped_column(String(64))
    model: Mapped[str] = mapped_column(String(128))
    input_tokens: Mapped[int]
    output_tokens: Mapped[int]
    cost_chf: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
