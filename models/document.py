from sqlalchemy import Column, Integer, String, Text, DateTime, text
from database import Base

class Document(Base):

    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    
    # PostgreSQL generates the date.. 
    upload_date = Column(DateTime, server_default=text("NOW()"), nullable=False)
    
    file_type = Column(String(10), nullable=False)
    extracted_text = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False)
    character_count = Column(Integer, nullable=False)
