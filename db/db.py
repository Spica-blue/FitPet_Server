from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from asyncpg import Connection
from uuid import uuid4
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class CConnection(Connection):
  def _get_unique_id(self, prefix: str) -> str:
    return f'__asyncpg_{prefix}_{uuid4()}__'

engine = create_async_engine(
  DATABASE_URL, 
  echo=True,
  connect_args={
    "statement_cache_size": 0,
    "connection_class": CConnection
  }
)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
  async with SessionLocal() as session:
    yield session

async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)

