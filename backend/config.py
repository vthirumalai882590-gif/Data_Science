"""
FIREGUARD X - Backend Application Configuration
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FIREGUARD X"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # In Vercel serverless functions, the root filesystem is read-only; use /tmp for SQLite
    _default_sqlite_path = (
        "/tmp/fireguard.db"
        if os.getenv("VERCEL")
        else os.path.join(BASE_DIR, "backend", "fireguard.db")
    )
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{_default_sqlite_path}")
    
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://*.vercel.app",
        "*"
    ]

settings = Settings()
