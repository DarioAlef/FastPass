from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os

load_dotenv()

class Settings(BaseSettings):
    db_host: str = os.getenv("DB_HOST")
    db_port: int = int(os.getenv("DB_PORT"))
    db_user: str = os.getenv("DB_USER")
    db_name: str = os.getenv("DB_NAME")
    db_password: str = os.getenv("DB_PASSWORD")
    
    
class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
        
settings = Settings()


DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)