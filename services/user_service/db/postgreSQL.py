from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DB_URL, DB_TEST_URL, DB_TEST
from db.base import BaseModelDB
from typing import AsyncGenerator

engine = create_async_engine(
    DB_TEST_URL if DB_TEST else DB_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModelDB.metadata.create_all)
