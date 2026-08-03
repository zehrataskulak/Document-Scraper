from .text_preprocessor import unicode_normalization

def extract_text_from_txt(file_path: str) -> str:
    try:
        # Opens as UTF-8 for Turkish/general character compatibility.
        with open(file_path, "r") as f:
            text = f.read()
        final_text = unicode_normalization(text)
        return final_text.strip()
        
    except Exception as e:
        print(f"An error occurred while reading the TXT file: {e}")
        return ""