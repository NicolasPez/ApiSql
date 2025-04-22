from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite+aiosqlite:///./tareas.db"

engine = create_engine(DATABASE_URL.replace("aiosqlite", "pysqlite"))
async_engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

database = Database(DATABASE_URL)
metadata = MetaData()

async def get_db():
    async with SessionLocal() as session:
        yield session
