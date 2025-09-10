from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    ACCESS_TTL_MIN: int = 15
    REFRESH_TTL_DAYS: int = 30
    CORS_ORIGINS: List[str] = ["*"]
    ENV: str = "development"
    OPENROUTER_KEY: str = ""


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
