import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

class Settings(BaseSettings):
    # Basic Project Settings
    # Temel Proje Ayarları
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "OrthopedicAI")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # Security Settings
    # Güvenlik Ayarları
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Database Settings
    # Veritabanı Ayarları
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./orthopedic.db")

    # AI Model Settings
    # Yapay Zeka Model Ayarları
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    class Config:
        case_sensitive = True

settings = Settings()