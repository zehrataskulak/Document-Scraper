import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    
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