import docx
from scraper.text_preprocessor import unicode_normalization

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        full_text = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)

        joined_text = "\n".join(full_text)

        final_text = unicode_normalization(joined_text)
        
        return final_text
        
    except Exception as e:
        print(f"An error occurred while reading the DOCX file: {e}")
        
        return ""