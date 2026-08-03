import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Create a configured database session factory linked to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class for mapping Python database models to SQL tables
Base = declarative_base()

# Import the model to ensure it is registered with Base before creating tables
from models.document import Document

# If the table does not exist, it creates it. if it does, it leaves it untouched
def init_db():
    Base.metadata.create_all(bind=engine)


# It opens a new session to the database for each API request then closes when the operation is complete.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()