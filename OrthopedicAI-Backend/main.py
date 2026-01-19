# OrthopedicAI-Backend/main.py

from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.core.database import engine, Base
from app.models import user 
# Import routers
# Yönlendiricileri içe aktar
from app.routers import auth, analysis

# Create database tables
# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include routers
# Yönlendiricileri dahil et
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(analysis.router, prefix=f"{settings.API_V1_STR}/analysis", tags=["analysis"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to OrthopedicAI Backend",
        "status": "running",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)