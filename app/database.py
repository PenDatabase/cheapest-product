from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from .config import settings

connect_args = {}
database_url = settings.DATABASE_URL

if database_url.startswith("postgres://"):
    database_url = settings.DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
if database_url.startswith("sqlite://"):
    connect_args = {"check_same_thread": False}

engine = create_engine(database_url, connect_args=connect_args)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass