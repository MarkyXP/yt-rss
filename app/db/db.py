from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(bind=engine)


def create_db_and_tables():
    """
    Imports all of the SQLModel schemas and creates the tables
    if they don't already exist.
    Note that this is called synchronously, so it needs to create its own engine
    """
    from app.schemas.channel_list import YT_Channel
    from app.schemas.videos import Videos
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, connect_args=connect_args)

    SQLModel.metadata.create_all(engine)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


create_db_and_tables()
