from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_ignore_empty=True)

    llm_provider: Literal["dummy", "openai_compatible"] = "dummy"
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    # Send the response schema as response_format "json_schema" (Decisions D-22).
    llm_structured_output: bool = True
    # Strict adherence only supports a subset of JSON Schema. Off until tested against our schemas.
    llm_strict_schema: bool = False
    # "none" turns off the model's thinking, which saves tokens. Not every model accepts this parameter.
    llm_reasoning_effort: Literal["none", "low", "medium", "high"] | None = None
    # Caps output tokens per call, reasoning included (docs/Security.md S2).
    llm_max_completion_tokens: int | None = 4096

    database_url: str = "mysql+pymysql://cvtailor:cvtailor@localhost:3306/cvtailor?charset=utf8mb4"
    cors_origins: list[str] = ["http://localhost:3000"]
    # Caps token cost per request (docs/Security.md S2).
    max_input_chars: int = 20_000


settings = Settings()
