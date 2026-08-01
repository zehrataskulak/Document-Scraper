import docx

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        extracted_text = []

        for paragraph in doc.paragraphs:
            if paragraph.text:
                extracted_text.append(paragraph.text)

        return "\n".join(extracted_text).strip()
        
    except Exception as e:
        print(f"An error occurred while reading the DOCX file: {e}")
        return ""
