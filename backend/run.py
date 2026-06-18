from fastapi import FastAPI

app = FastAPI(title="AfterMarket Core Engine")

@app.get("/healthz")
def health_check():
    return {"status": "healthy", "engine": "active"}