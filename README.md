# Python Data Scraper Web Application

A web application developed for the Software Engineering Internship Technical Assessment. It allows users to upload documents (PDF, DOCX, TXT), automatically extracts their textual content, applies comprehensive data preprocessing, and securely stores the structured metadata in a database.

---

## 🏗 Architecture & Project Structure

The project follows a modular architecture separating the API/Web layer, database models, and document parsing logic. This ensures maintainability and scalability.

project/
├── app.py                    # Main backend application and routes
├── database.py               # Database configuration and session management
├── models/
│   └── document.py           # Relational database schema
├── scraper/
│   ├── docx_reader.py        # DOCX text extraction
│   ├── pdf_reader.py         # PDF text extraction
│   ├── txt_reader.py         # Plain TXT extraction
│   └── text_preprocessor.py  # Data cleaning and normalization
├── templates/                # HTML frontend layout
├── uploads/                  # Sample testing documents
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation

---

## 🛠 Technologies Used

- Backend: Python (FastAPI)
- Database ORM: SQLAlchemy
- Database Systems: PostgreSQL (Production) & SQLite (Local testing)
- Document Parsing: pdfplumber, python-docx
- Preprocessing: Python standard 're' (Regex) module

---

## 🗄 Database Design & Justification

### Stored Attributes
- Document ID, Original Filename, Upload Date, File Type, Extracted Text, Word Count, Character Count.

### PostgreSQL vs. SQLite Justification
While SQLite can be used for lightweight local development, PostgreSQL is the definitively chosen system for this project's production environment. PostgreSQL provides Multi-Version Concurrency Control (MVCC) which prevents database locking during simultaneous file uploads, and it offers superior indexing capabilities (like GIN/GiST) for large text storage and search operations compared to SQLite.

---

## ⚙ Data Preprocessing

The text preprocessing pipeline handles the following operations to ensure data quality:
- Removes multiple spaces, empty lines, and tabs.
- Normalizes line endings and Unicode characters.
- Accurately computes exact word and character counts.

---

## 🚀 Installation & Execution Instructions

1. Set Up the Virtual Environment:
   python3 -m venv venv
   source venv/bin/activate  (On Windows: .\venv\Scripts\Activate.ps1)

2. Install Dependencies:
   pip install -r requirements.txt

3. Start Database Service (If using PostgreSQL on Linux/WSL):
   sudo service postgresql start

4. Run the Application:
   uvicorn app:app --reload  (or equivalent command for Flask: python app.py)

5. Access the Platform:
   Open your browser and go to http://127.0.0.1:8000 

---

## 🤖 Responsible AI Usage

AI tools (Gemini/ChatGPT) were utilized strictly as development assistants to enhance productivity and maintain code quality throughout the project lifecycle.
- Code Optimization: Used AI to review and refine the text preprocessing pipelines, regular expressions, and database queries.
- Debugging & Troubleshooting: Leveraged AI to quickly diagnose local environment configuration issues and database connection errors during testing.
- Documentation: Assisted in structuring the project documentation and articulating technical design choices clearly.

