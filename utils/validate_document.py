import os
import magic
from fastapi import HTTPException, UploadFile, status

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt"
}

def validate_file_format(file_path: str, filename: str) -> str:
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid file extension ({file_ext}). Supported: PDF, DOCX, TXT."
        )

    # Actual Content (MIME) Check
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(file_path)

    # Check if file MIME type is allowed and matches extension, otherwise reject as mismatch or unsupported
    if (file_mime in ALLOWED_MIME_TYPES and ALLOWED_MIME_TYPES[file_mime] != file_ext) or (file_mime not in ALLOWED_MIME_TYPES):
        actual_format = ALLOWED_MIME_TYPES.get(file_mime, file_mime)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extension mismatch detected. The file content is in '{actual_format}' format or is corrupt, but it is labeled as '{file_ext}'."
        )

    return file_ext


def validate_document_content(text: str, filename: str) -> str:
    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The uploaded file '{filename}' is completely empty (0 KB). Please upload a valid document."
        )
    return text.strip()


def validate_file_size(file: UploadFile, max_size_mb: int):
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # Move file pointer to the end to get total size in bytes
    file.file.seek(0, 2)
    file_size = file.file.tell()
    
    # Reset file pointer back to the beginning for further reading
    file.file.seek(0)
    
    # Check if file size exceeds the allowed limit
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size is too large! The uploaded file exceeds the {max_size_mb} MB limit."
        )
        
    return file_size
