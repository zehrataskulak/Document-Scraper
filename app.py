import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session

from scraper.text_preprocessor import clean_text, get_text_metrics
from scraper.extract_and_save import extract_text_by_type, save_uploaded_file
from database import init_db, Document, get_db

from utils.validate_document import validate_file_format, validate_document_content, validate_file_size


app = FastAPI(title="Document Data Scraper")

init_db()

# Initialize Jinja2 template engine to render HTML files from the templates directory
templates = Jinja2Templates(directory="templates")

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

UPLOAD_DIR = "uploads"


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")



@app.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    validate_file_size(file, max_size_mb=5)

    # 1. Dosyayı geçici/kalıcı klasöre kaydet
    file_path = await save_uploaded_file(file, UPLOAD_DIR)
    
    try:
        # 2. Uzantıyı ve Gerçek Dosya Yapısını (Sahtecilik Kontrolü) Doğrula
        file_ext = validate_file_format(file_path, file.filename)
        
        # 3. Metni dökümandan kazı
        text_read = extract_text_by_type(file_path, file_ext)
        
        # 4. Metni temizle
        extracted_text = clean_text(text_read)
        
        # 5. Boş döküman kontrolünü gerçekleştir
        validated_text = validate_document_content(extracted_text, file.filename)
        
        # 6. Metrikleri hesapla
        metrics = get_text_metrics(validated_text)
        word_count, character_count = metrics["word_count"], metrics["character_count"]
        
        # 7. Veritabanı modelini oluştur ve kaydet
        new_document = Document(
            original_filename=file.filename,
            file_type=file_ext,
            extracted_text=validated_text,
            word_count=word_count,
            character_count=character_count
        )
        
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        return {
            "document_id": new_document.document_id,
            "filename": file.filename,
            "file_type": file_ext,
            "word_count": word_count,
            "character_count": character_count,
            "extracted_text": validated_text
        }
        
    except HTTPException as http_exc:
        # Eğer validasyonlarda bir hata çıktıysa diske yazılan hatalı/boş dosyayı temizle
        if os.path.exists(file_path):
            os.remove(file_path)
        raise http_exc
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"A system error occurred: {str(e)}")


# Fetches all database records sorted by newest document first
@app.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.document_id.desc()).all()