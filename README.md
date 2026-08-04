# Python Data Scraper Web Application

A web application developed for the Software Engineering Internship Technical Assessment. It allows users to upload documents (PDF, DOCX, TXT), automatically extracts their textual content, applies preprocessing, and stores the structured metadata in a database.

---

## 🏗 Architecture & Project Structure

The project follows a modular architecture that separates the API/web layer, persistence layer, and document parsing logic.

project/
├── app.py                    # Main FastAPI application and routes
├── database.py               # Database configuration and session management
├── models/
│   └── document.py           # Relational schema for stored documents
├── scraper/
│   ├── docx_reader.py        # DOCX extraction logic
│   ├── pdf_reader.py         # PDF extraction logic
│   ├── txt_reader.py         # TXT extraction logic
│   ├── extract_and_save.py   # Upload handling and file saving
│   └── text_preprocessor.py  # Text cleaning and metrics
├── templates/                # HTML frontend interface
├── uploads/                  # Sample testing documents (PDF, DOCX, TXT)
├── utils/
│   └── validate_document.py  # File validation and safety checks
├── requirements.txt          # Project dependencies
├── sample_database.sql       # Sample PostgreSQL seed data
└── README.md                 # Project documentation

---

## 🛠 Technologies Used

- Backend: Python (FastAPI)
- Database ORM: SQLAlchemy
- Database System: PostgreSQL for production-style usage
- Document Parsing: pdfplumber, python-docx
- File Validation: python-magic
- Preprocessing: Python standard regex and text normalization utilities

---

## 🗄 Database Design & Justification

### Stored Attributes
- Document ID
- Original Filename
- Upload Date
- File Type
- Extracted Text
- Word Count
- Character Count

### Why PostgreSQL was chosen
PostgreSQL is the recommended database for this project because it is more suitable for concurrent uploads, larger text storage, and future search/indexing features than SQLite. It also provides better support for production-style deployments and data integrity.

### Sample Database
A sample PostgreSQL seed script is available in [sample_database.sql](sample_database.sql). It creates a documents table and inserts three example records for testing and demonstration.

You can load it with:
```bash
psql -U document_user -d document_scraper -f sample_database.sql
```

---

## ⚙ Data Preprocessing

The preprocessing pipeline performs the following operations:
- Removes extra whitespace, empty lines, and tabs
- Normalizes line endings and Unicode characters
- Computes exact word and character counts

---

## 🚀 Installation & Execution Instructions

1. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Create a PostgreSQL database:
   sudo -u postgres psql
   CREATE DATABASE document_scraper;
   CREATE USER document_user WITH PASSWORD 'your_password';
   ALTER ROLE document_user WITH SUPERUSER;
   GRANT ALL PRIVILEGES ON DATABASE document_scraper TO document_user;

4. Configure the environment variable:
   Create a .env file with:
   DATABASE_URL=postgresql://document_user:your_password@localhost:5432/document_scraper

5. Initialize the database tables:
   python -c "from database import init_db; init_db()"

6. Run the application:
   uvicorn app:app --reload

7. Open the app:
   http://127.0.0.1:8000

### Optional: load sample data
Run the following command after connecting to PostgreSQL:
psql -U document_user -d document_scraper -f sample_database.sql

---

## 🤖 Responsible AI Usage

AI tools were used as development assistants to improve productivity and code quality.
- Code review and cleanup
- Debugging environment and database issues
- Documentation drafting and structure improvement
- Suggesting validation and database-design improvements

Example prompts are stored in [docs/ai_prompts.md](docs/ai_prompts.md).

---

## 🧩 Generated vs. Manually Modified Code

The base project structure and core implementation were created during development, while the following items were adjusted manually to match the project requirements:
- README documentation and project explanation
- Upload validation messaging and UI behavior
- Database setup instructions and sample data script
- Bonus documentation sections for AI usage, future improvements, and sample data

---

## 🔮 Future Improvements

Possible next steps for the project include:
- Add search and filtering for uploaded documents
- Support more file formats such as DOC and XLSX
- Improve OCR support for scanned PDFs
- Add authentication and user management
- Add unit and integration tests
- Improve database indexing for faster text search
- Add export features for extracted text and metadata
- Add user roles and audit logging for uploaded documents

