# OrthopedicAI-Backend/app/services/image_service.py

import shutil
import uuid
import os
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

# Define the temporary upload directory
# Geçici yükleme dizinini tanımla
UPLOAD_DIR = Path("temp_uploads")

def validate_image(file: UploadFile) -> None:
    """
    Validates if the uploaded file is a supported image type.
    Yüklenen dosyanın desteklenen bir resim türü olup olmadığını doğrular.
    """
    # Allowed content types for Gemini (JPEG, PNG, WEBP, HEIC, HEIF)
    # Gemini için izin verilen içerik türleri (JPEG, PNG, WEBP, HEIC, HEIF)
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp", "image/heic", "image/heif"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )

def save_upload_file(file: UploadFile) -> str:
    """
    Saves the uploaded file to a temporary directory with a unique name.
    Yüklenen dosyayı benzersiz bir adla geçici bir dizine kaydeder.
    """
    # Create directory if it doesn't exist
    # Eğer dizin yoksa oluştur
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate a unique filename to prevent overwrites
    # Üzerine yazmayı önlemek için benzersiz bir dosya adı oluştur
    # We use uuid to ensure uniqueness
    # Benzersizliği sağlamak için uuid kullanıyoruz
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save the file content
        # Dosya içeriğini kaydet
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        # Remove the file if error occurs
        # Hata oluşursa dosyayı kaldır
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
            
    return str(file_path)

def delete_file(file_path: str) -> None:
    """
    Deletes the file from the filesystem after processing.
    İşlemden sonra dosyayı dosya sisteminden siler.
    """
    path = Path(file_path)
    if path.exists():
        os.remove(path)