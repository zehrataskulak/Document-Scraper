import os
import magic
from fastapi import HTTPException, UploadFile, status
from models.document import Document

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt"
}

def validate_file_format(file_path: str, filename: str) -> str:
    file_ext = os.path.splitext(filename)[1].lower()
    
    # 1. Aşama: Uzantı Kontrolü
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid file extension ({file_ext}). Supported: PDF, DOCX, TXT."
        )

    # 3. Aşama: Gerçek İçerik (MIME) Kontrolü
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(file_path)

    # 4. Aşama: Uzantı ve İçerik Uyuşuyor mu? (Sahtecilik Kontrolü)
    # Koşul A: Bulunan MIME tipi izin verilenlerde var ama yüklenen uzantı ile uyuşmuyor
    # Koşul B: Bulunan MIME tipi izin verilenler listesinde hiç yok (Örn: .exe, .png)
    if (file_mime in ALLOWED_MIME_TYPES and ALLOWED_MIME_TYPES[file_mime] != file_ext) or (file_mime not in ALLOWED_MIME_TYPES):
        actual_format = ALLOWED_MIME_TYPES.get(file_mime, file_mime)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extension mismatch detected. The file content is in '{actual_format}' format or is corrupt, but it is labeled as '{file_ext}'."
        )

    return file_ext

def validate_document_content(text: str, filename: str) -> str:
    """
    Metnin boş olup olmadığını kontrol eder. 
    Sadece boşluklardan oluşan metinleri de temizleyerek yakalar.
    """
    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The uploaded file '{filename}' is completely empty (0 KB). Please upload a valid document."
        )
    return text.strip()




def validate_file_size(file: UploadFile, max_size_mb: int):
    """
    Yüklenen dosyanın boyutunu kontrol eder. 
    Belirlenen limiti aşarsa hata fırlatır.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # 1. İmleci dosyanın en sonuna (2: os.SEEK_END) gönderip konumu bayt olarak okuyoruz
    file.file.seek(0, 2)
    file_size = file.file.tell()
    
    # 2. Dosyanın daha sonra kazıcılar (scraper) tarafından okunabilmesi için 
    # imleci tekrar en başa (0) alıyoruz
    file.file.seek(0)
    
    # 3. Boyut kontrolü yapılıyor
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size is too large! The uploaded file exceeds the {max_size_mb} MB limit."
        )
        
    return file_size
