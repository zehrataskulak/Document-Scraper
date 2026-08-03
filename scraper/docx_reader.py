import docx
import unicodedata # Normalizasyon kullanıyorsan

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        full_text = []
        
        # Paragrafları listeye ekliyoruz
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
                
        # 1. HATA BURADAYDI: full_text bir listeydi. 
        # Önce listeyi satır satır birleştirip tek bir string (metin) yapıyoruz:
        joined_text = "\n".join(full_text)
        
        # 2. Normalizasyon işlemini (NFC/NFD) liste üzerinde değil, birleşik metin üzerinde yapıyoruz:
        normalized_text = unicodedata.normalize("NFC", joined_text)
        
        return normalized_text
        
    except Exception as e:
        print(f"An error occurred while reading the DOCX file: {e}")
        # Hata anında uygulamanın çökmemesi için boş dönüyor, ama artık hata almayacaksın!
        return ""