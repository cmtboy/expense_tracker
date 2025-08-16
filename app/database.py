# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Special path for Render compatibility
SQLITE_PATH = "/tmp/expense_tracker.db" if 'RENDER' in os.environ else "./expense_tracker.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()