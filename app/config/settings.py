from pydantic_settings import BaseSettings
from typing import Set


class Settings(BaseSettings):
    DATABASE_URL: str

    ALLOWED_FILE_EXTENSIONS: Set[str] = {
        ".docx",
        ".doc",
        ".pdf",
        ".txt",
        ".md",
    }

    class Config:
        env_file = ".env"


settings = Settings()
