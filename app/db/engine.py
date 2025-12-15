import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv('USER_NAME')
DB_PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("One or more database environment variables are not set")
    raise RuntimeError("Database environment variables not set properly")

DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Use SQLAlchemy sync engine for now; switching to async is straightforward later
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def init_db():
    print("Creating database tables...")
    from app.db import models
    models.Base.metadata.create_all(bind=engine)
