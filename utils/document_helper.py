import os
import magic  # pip install python-magic
from fastapi import HTTPException, UploadFile, status
from models.document import Document

from scraper.pdf_reader import extract_text_from_pdf
from scraper.docx_reader import extract_text_from_docx
from scraper.txt_reader import extract_text_from_txt

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
            detail=f"Geçersiz dosya uzantısı ({file_ext}). Desteklenenler: PDF, DOCX, TXT."
        )

    # 2. Aşama: Fiziksel Boş Dosya Kontrolü (Kesin Çözüm)
    # Magic kütüphanesinin 'empty' sonuçlarıyla uğraşmak yerine doğrudan disk boyutuna bakıyoruz
    if os.path.getsize(file_path) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Yüklenen '{filename}' dosyası tamamen boş (0 KB). Lütfen geçerli bir döküman yükleyin."
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
            detail=f"Uzantı çelişkisi algılandı. Dosya içeriği '{actual_format}' yapısında veya bozuk, ancak '{file_ext}' olarak etiketlenmiş."
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
            detail=f"Yüklenen '{filename}' dosyası tamamen boş (0 KB). Lütfen geçerli bir döküman yükleyin."
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
            detail=f"Dosya boyutu çok büyük! Yüklenen dosya {max_size_mb} MB sınırını aşıyor."
        )
        
    return file_size




def extract_text_by_type(file_path: str, file_ext: str) -> str:
    """Dosya türüne göre doğru kazıma (scraper) fonksiyonunu tetikler."""
    if file_ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return extract_text_from_txt(file_path)


    

async def save_uploaded_file(file: UploadFile, upload_dir: str) -> str:
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        buffer.flush()  # Disk arabelleğini tamamen temizle
    return file_path