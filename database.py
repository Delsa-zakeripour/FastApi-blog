# from sqlalchemy import  create_engine 
import asyncio

from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from alembic import command
from config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" the comment are the code befor async 
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(settings.database_url)
# SessionLocal = sessionmaker(autocommit= False, authoflush= False, bind=engine)
AsyncSessionLocal = async_sessionmaker(engine, class_= AsyncSession, expire_on_commit=False,  )

class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def run_migrations() -> None:
    """Apply pending Alembic migrations (runs sync Alembic in a worker thread)."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    # command.upgrade uses asyncio.run via env.py; run in a thread to avoid
    # conflicting with FastAPI's already-running event loop.
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
