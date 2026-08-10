import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

db_url = settings.DATABASE_URL

# If running locally on Windows and using a standard postgresql, route via pg8000 to bypass psycopg2 errors
if os.name == "nt" and db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+pg8000://")


# Pool parameters are fine-tuned for high concurrency stability 
engine = create_engine(
    db_url,                 # Pass the adapted db_url here instead
    pool_size=20,           # Keeps 20 persistent connections open to eliminate handshake lag
    max_overflow=10,        # Dynamically scales up an extra 10 connections under sudden traffic spikes
    pool_pre_ping=True      # Automatically tests connections before queries to prevent deadlocks
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency generator that yields an isolated database session
    and guarantees its safe closure after request execution
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()