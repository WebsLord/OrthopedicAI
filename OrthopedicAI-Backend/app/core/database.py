from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the database engine for SQLite
# SQLite için veritabanı motorunu oluştur
# "check_same_thread": False is needed strictly for SQLite
# "check_same_thread": False sadece SQLite için gereklidir
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
# Yapılandırılmış bir "Session" (Oturum) sınıfı oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from
# Modellerimizin miras alacağı temel sınıf
Base = declarative_base()

# Dependency to get the database session
# Veritabanı oturumunu almak için bağımlılık
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()