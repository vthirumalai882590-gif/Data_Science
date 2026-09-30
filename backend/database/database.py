"""
FIREGUARD X - Database Connection Management
Uses SQLAlchemy 2.0 with support for SQLite and seamless portability to PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

import os
import shutil

# If running on Vercel and using /tmp, copy existing template database if available
if os.getenv("VERCEL") and "/tmp/fireguard.db" in settings.DATABASE_URL:
    tmp_path = "/tmp/fireguard.db"
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fireguard.db")
    if not os.path.exists(tmp_path) and os.path.exists(template_path):
        try:
            shutil.copyfile(template_path, tmp_path)
        except Exception:
            pass

# For SQLite, check_same_thread is False to allow FastAPI multi-threaded requests
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI Dependency for database session life-cycle."""
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
