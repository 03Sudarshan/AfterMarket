from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Pool parameters are fine-tuned for high concurrency stability 
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,               # Keeps 20 persistent connections open to elimianate handshake lag
    max_overflow=10,            # Dynamically scales up an extra 10 connections under sudden traffic spikes
    pool_pre_ping=True          # Automatically tests connections before queries to prevent dead locks 
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