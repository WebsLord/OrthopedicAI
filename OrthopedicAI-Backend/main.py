from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.core.database import engine, Base
# Import models explicitly so SQLAlchemy detects them
# Modelleri açıkça içe aktar, böylece SQLAlchemy onları algılar
from app.models import user 

# Create database tables
# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to OrthopedicAI Backend",
        "status": "running",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)