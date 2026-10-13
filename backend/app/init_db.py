"""Create the tables: `python -m app.init_db`. To be replaced by Alembic migrations once the schema settles."""

from app import models  # noqa: F401  (registers the tables on Base.metadata)
from app.db import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created:", ", ".join(Base.metadata.tables))
