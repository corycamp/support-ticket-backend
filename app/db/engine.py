import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv('USER_NAME')
DB_PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_URL = os.getenv('DB_URL')

engine = None
SessionLocal = None

# Prefer an explicit DATABASE_URL env var; otherwise attempt to build one from individual vars.
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL and all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    DATABASE_URL = f'{DB_URL}{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# If still not set, fall back to a local SQLite DB so tests and dev environment work without Postgres.
# if not DATABASE_URL:
#     print("One or more database environment variables are not set; falling back to SQLite dev DB")
#     DATABASE_URL = os.getenv('SQLITE_DATABASE_URL', 'sqlite:///./dev.db')

def init_db():
    print("Setting up database...")

    if not DATABASE_URL:
        print("Database URL not set; skipping database initialization.")
        raise ValueError("Database URL not set")

    global engine, SessionLocal
    engine = create_engine(DATABASE_URL, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    
    from app.db import models
    models.Base.metadata.create_all(bind=engine)

def close_db():
    global engine
    if engine:
        engine.dispose()
        engine = None
        print("Database connection closed.")