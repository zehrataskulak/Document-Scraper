import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    try:
        extracted_text = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)

        return "\n".join(extracted_text).strip()

    except Exception as e:
        print(f"An error occurred while reading the PDF file: {e}")
        return ""
