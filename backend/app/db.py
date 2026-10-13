from collections.abc import Iterator
from typing import ClassVar

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# No connection is opened until the first query, so the API runs without MySQL until a feature needs it.
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    # utf8mb4 on every table: MySQL's legacy "utf8" can't store all characters (docs/Decisions.md D-11).
    __table_args__: ClassVar[dict] = {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_0900_ai_ci"}


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
