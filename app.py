import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session

from scraper.text_preprocessor import clean_text, get_text_metrics
from scraper.pdf_reader import extract_text_from_pdf
from scraper.docx_reader import extract_text_from_docx
from scraper.txt_reader import extract_text_from_txt
from database import init_db, Document, get_db


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

    file_ext = os.path.splitext(file.filename)[1].lower()
        
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid format ({file_ext}). Supported types: PDF, DOCX, TXT."
        )

    # Create the path where the file will be saved
    file_path =  os.path.join(UPLOAD_DIR, file.filename)

    # Open the file in binary write mode and save the content.
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    if file_ext == ".pdf":
        text_read = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        text_read = extract_text_from_docx(file_path)
    else:
        text_read = extract_text_from_txt(file_path)


    extracted_text = clean_text(text_read)
    metrics = get_text_metrics(extracted_text)
    word_count, character_count = metrics["word_count"], metrics["character_count"]


    new_document = Document(
        original_filename=file.filename,
        file_type=file_ext,
        extracted_text=extracted_text,
        word_count=word_count,
        character_count=character_count
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document) # refresh to retrieve the auto-generated ID

    return {
        "document_id": new_document.document_id,
        "filename": file.filename,
        "file_type": file_ext,
        "word_count": word_count,
        "character_count": character_count,
        "extracted_text": extracted_text
    }


# Fetches all database records sorted by newest document first
@app.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.document_id.desc()).all()