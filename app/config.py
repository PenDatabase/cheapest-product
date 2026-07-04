import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()