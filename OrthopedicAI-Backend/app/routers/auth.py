from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas import user as user_schema

router = APIRouter()

# 1. REGISTER ENDPOINT
@router.post("/register", response_model=user_schema.User)
def register_new_user(
    user_in: user_schema.UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create new user.
    Yeni kullanıcı oluştur.
    """
    # Check if user already exists
    # Kullanıcının zaten var olup olmadığını kontrol et
    user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Create new user instance
    # Yeni kullanıcı örneği oluştur
    user = UserModel(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
    )
    
    # Add to DB
    # Veritabanına ekle
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 2. LOGIN ENDPOINT
@router.post("/login", response_model=user_schema.Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    OAuth2 uyumlu token girişi, gelecek istekler için erişim tokenı al.
    """
    # Find user by email
    # Kullanıcıyı e-posta ile bul
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # Authenticate
    # Kimlik doğrulama
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create Access Token
    # Erişim Tokenı oluştur
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }