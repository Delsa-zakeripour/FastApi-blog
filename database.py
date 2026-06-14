# from sqlalchemy import  create_engine 
from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" the comment are the code befor async 
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {'check_same_thread':False},
)

# SessionLocal = sessionmaker(autocommit= False, authoflush= False, bind=engine)
AsyncSessionLocal = async_sessionmaker(engine, class_= AsyncSession, expire_on_commit=False,  )

class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  