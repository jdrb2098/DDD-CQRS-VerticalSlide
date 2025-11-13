from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from asisya_api.core.config import settings
from passlib.context import CryptContext


SQLALCHEMY_DATABASE_URL = settings.database_url

# Sólo usar check_same_thread para SQLite
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# Engine sync (Postgres sync driver: postgresql://user:pass@host:port/db)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
