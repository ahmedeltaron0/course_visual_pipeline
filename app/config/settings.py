from pydantic_settings import BaseSettings
from typing import Set, Optional


class Settings(BaseSettings):

    # Database
    DATABASE_URL: Optional[str] = None

    # Supabase
    PROJECT_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SECRECT_KEY: Optional[str] = None

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Higgsfield
    HF_API_KEY: Optional[str] = None
    HF_API_SECRET: Optional[str] = None

    # Files
    ALLOWED_FILE_EXTENSIONS: Set[str] = {
        ".docx",
        ".doc",
        ".pdf",
        ".txt",
        ".md",
    }

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
