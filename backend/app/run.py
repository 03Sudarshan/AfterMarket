from fastapi import FastAPI
from app.core.database import engine
from app.core import database

# Instructs the database engine to generate all tables declared in our schemas if they don't exist. 
# Note: For later production iterations we will scale this out into automated Alembic migrations.
try:
    database.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization hook paused or skipped during pipeline isolated check: {e}")

app = FastAPI(title="AfterMarket Core Engine")

@app.get("/healthz")
def health_check():
    """
    Standard automated orchestration probe for container health monitoring.
    """
    return{"status": "healthy", "engine": "active"}