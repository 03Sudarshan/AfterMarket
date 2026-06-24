import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, get_db
from app.core import database

# Instructs the database engine to generate all tables declared in our schemas if they don't exist. 
try:
    database.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization hook paused or skipped during pipeline isolated check: {e}")

app = FastAPI(title="AfterMarket Core Engine")

@app.get("/healthz")
def health_check():
    """
    Standard automated orchestration probe for container health monitoring (Shallow Check).
    """
    return {"status": "healthy", "engine": "active"}

@app.get("/api/health")
def deep_health_check(db: Session = Depends(get_db)):
    """
    Deep health check that executes an isolated low-overhead SQL query 
    to verify the active database connection pool.
    """
    try:
        # Execute a raw SQL test query to ping the database
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "FastAPI to PostgreSQL communication layer verified successfully!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection engine unreachable: {str(e)}"
        )