from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: Literal["dummy", "openai_compatible"] = "dummy"
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    # OpenAI-style JSON mode. Unverified for Infomaniak, so off by default (see docs/Decisions.md, open questions).
    llm_json_mode: bool = False

    database_url: str = "mysql+pymysql://cvtailor:cvtailor@localhost:3306/cvtailor?charset=utf8mb4"
    cors_origins: list[str] = ["http://localhost:3000"]
    # Caps token cost per request (docs/Security.md S2).
    max_input_chars: int = 20_000


settings = Settings()
