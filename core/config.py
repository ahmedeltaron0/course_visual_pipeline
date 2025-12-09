from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY : str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(..., env="OPENAI_MODEL")
    HF_API_KEY : str = Field(..., env="HF_API_KEY")
    HF_API_SECRET: str = Field(..., env="HF_API_SECRET")


    class Config:
        # Automatically read from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"
