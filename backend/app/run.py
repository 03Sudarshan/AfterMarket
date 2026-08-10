import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core import database
from app.core.database import engine, get_db
from app.api.routes.market import router as market_router

# 1. Initialize the core FastAPI Application instance first
app = FastAPI(title="AfterMarket Core Engine")

# 2. Safely trigger database table creation hooks
try:
    database.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization hook paused or skipped during pipeline isolated check: {e}")

# 3. Register your marketplace business engine routes
app.include_router(market_router)


# ========================================================
# HEALTH & MONITORING ENDPOINTS
# ========================================================

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