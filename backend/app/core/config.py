import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manages application-wide configuration state using environment variables
    """
    PROJECT_NAME: str = "AfterMarket Backend Engine"
    API_V1_STR: str = "/api/v1"

    # Database Configuration Anchors
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "local_secure_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "aftermarket_dev")
    DATABASE_URL: Optional[str] = None

    class Config:
        case_sensitive = True
    
settings = Settings()

# Dynamically construct standard connection string format
settings.DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"