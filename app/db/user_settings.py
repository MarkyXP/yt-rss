"""
# References:
> https://fastapi.tiangolo.com/tutorial/sql-databases
"""

import asyncio

import fastapi
import httpx
import sqlmodel
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import channel_list
from app.web_queries import yt_handler


async def add_channel(
    channel_name: str, db: AsyncSession, web_client: httpx.AsyncClient
) -> int:
    """
    Checks if a youtube channel exists, if it does it adds it to the database of
    channels, and returns the channel ID.
    If there is an error it returns -1.
    """
    url_exists = await yt_handler.check_channel_exists(channel_name, web_client)
    if not url_exists:
        return -1
    channel = channel_list.YT_Channel(channel_handle=channel_name)
    db.add(channel)
    await db.commit()
    return channel.id


async def list_channels(offset: int, limit: int, db: AsyncSession):
    channels = await db.execute(
        sqlmodel.select(channel_list.YT_Channel).offset(offset).limit(limit)
    ).all()
    return channels


def remove_channel(channel_id: int, db=sqlmodel.Session):
    channel = db.get(channel_list.YT_Channel, channel_id)
    if not channel:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Channel ID '{channel_id}' not found"
        )
    db.delete(channel)
    db.commit()
