import re
import unicodedata


def _remove_control_characters(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)


def unicode_normalization(raw_text: str) -> str:
    # 1. Karakterleri web ve veritabanı standardı olan NFC formuna normalize et
    normalized_text = unicodedata.normalize('NFC', raw_text)

    # 2. Remove embedded NUL/control characters that break database inserts
    sanitized_text = _remove_control_characters(normalized_text)

    # 3. Diğer temizlik işlemlerini yap (boşlukları silme vb.)
    cleaned_text = sanitized_text.strip()

    return cleaned_text


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = _remove_control_characters(text)

    # Standardize line breaks and tabs
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\t", " ")
    
    # Reduces consecutive blank lines to a single line
    text = re.sub(r"\n\s*\n+", "\n", text)
    
    # Converts consecutive spaces into a single space
    text = re.sub(r" +", " ", text)
    
    # Trims the beginning and the end
    extracted_text = text.strip()
    return extracted_text



def get_text_metrics(text: str) -> dict:
    if not text:
        return {"word_count": 0, "character_count": 0}
        
    char_count = len(text)
    
    words = text.split()
    word_count = len(words)
    
    return {
        "word_count": word_count,
        "character_count": char_count
    }