-- Sample PostgreSQL seed data for the Document Scraper project
-- Run this after creating the database and setting DATABASE_URL.

CREATE TABLE IF NOT EXISTS documents (
    document_id SERIAL PRIMARY KEY,
    original_filename VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    extracted_text TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    character_count INTEGER NOT NULL
);

INSERT INTO documents (original_filename, file_type, extracted_text, word_count, character_count)
VALUES
    (
        'Technical_Assessment_Python_Data_Scraper_Internship.pdf',
        '.pdf',
        'This sample PDF document represents the internship assessment requirements and demonstrates the upload and extraction flow.',
        16,
        131
    ),
    (
        'z13.docx',
        '.docx',
        'This sample DOCX file shows how the parser handles Microsoft Word documents.',
        12,
        92
    ),
    (
        'zz2.txt',
        '.txt',
        'This sample TXT file is used to validate plain text uploads and preprocessing.',
        11,
        85
    );
