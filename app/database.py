from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from .config import settings

connect_args = {}
database_url = settings.DATABASE_URL

if database_url.startswith("postgres://"):
    database_url = settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
if database_url.startswith("sqlite://"):
    database_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://", 1)
    connect_args = {"check_same_thread": False}

engine = create_async_engine(database_url, connect_args=connect_args)

SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass