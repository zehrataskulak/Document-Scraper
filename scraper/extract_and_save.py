import os
from fastapi import UploadFile

from scraper.pdf_reader import extract_text_from_pdf
from scraper.docx_reader import extract_text_from_docx
from scraper.txt_reader import extract_text_from_txt



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