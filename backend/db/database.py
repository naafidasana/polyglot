from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from urllib.parse import quote_plus
from ..config import Settings

settings = Settings()
db_password = quote_plus(settings.db_password)
DB_URL = f"postgresql://{settings.db_username}:{db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# DB dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()
