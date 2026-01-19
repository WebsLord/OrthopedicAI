from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
# Ortak özellikler
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

# Properties to receive via API on creation
# Oluşturma sırasında API üzerinden alınacak özellikler
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties to return to client
# İstemciye (client) döndürülecek özellikler
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# --- NEW ADDITIONS / YENİ EKLEMELER ---

# Schema for JWT Token response
# JWT Token yanıtı için şema
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for Token payload
# Token içeriği için şema
class TokenData(BaseModel):
    email: Optional[str] = None