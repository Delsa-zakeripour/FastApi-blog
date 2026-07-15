# from sqlalchemy import  create_engine 
from alembic import context
from alembic.config import Config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine, async_sessionmaker, async_engine_from_config
from sqlalchemy.orm import DeclarativeBase
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
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)

    connectable = async_engine_from_config(
        alembic_cfg.get_section(alembic_cfg.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()