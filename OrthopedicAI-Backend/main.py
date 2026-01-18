from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.routers import auth, analysis

# Initialize the FastAPI application
# FastAPI uygulamasını başlat
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Root endpoint to test if server is running
# Sunucunun çalışıp çalışmadığını test etmek için kök uç noktası
@app.get("/")
def read_root():
    return {
        "message": "Welcome to OrthopedicAI Backend",
        "status": "running",
        "docs_url": "/docs"
    }

# Include routers (We will enable these later as we build them)
# Yönlendiricileri dahil et (Bunları oluşturdukça aktif edeceğiz)
# app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
# app.include_router(analysis.router, prefix=f"{settings.API_V1_STR}/analysis", tags=["analysis"])

# Entry point for running the application directly
# Uygulamayı doğrudan çalıştırmak için giriş noktası
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)