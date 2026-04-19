"""
The interactions with the YouTube channels
"""

import asyncio
from contextlib import asynccontextmanager
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends

from app.db import db
from app.workflow.ingest import ingest_rss_feed
from app.workflow import subscription_management

import httpx

# @asynccontextmanager
async def get_http_client():# -> asyncio.AsyncGenerator[httpx.AsyncClient]:
    """
    An asynchronous dependency that provides an httpx.AsyncClient.

    The client is created within an async context manager (async with), 
    ensuring it is properly closed when the request is done.
    """
    async with httpx.AsyncClient() as client:
        yield client

router = APIRouter()

@router.post("/add_subscription")
async def add_subscription(
    channel_name : str,
    db_conn = Depends(db.get_db_connection),
    session : httpx.AsyncClient = Depends(get_http_client)
) -> str:
    """
    Adds a new subscription to the database and periodically fetches the RSS feed from YouTube.

    Args:
        - channel_name (str) : The Youtube channel's name (e.g. eevblog) or its link (e.g. https://www.youtube.com/eevblog)

    Returns:
        - The YouTube Channel ID (e.g. UCBw76458901234567890)
    """
    return await subscription_management.add_subscription(
        session = session,
        db_conn = db_conn,
        channel_name = channel_name
    )

@router.post("/update_channels")
async def update_channels(
    channel_ids : list[str] | None = None,
    db_conn = Depends(db.get_db_connection),
    client : httpx.AsyncClient = Depends(get_http_client)
):
    await asyncio.gather(
        *[ingest_rss_feed(
            session = client,
            db_conn = db_conn,
            channel_id = channel_id
        ) for channel_id in channel_ids]
    )

@router.get("/update_all_subscribed_channels")
async def update_all_subscribed_channels(
    background_tasks: BackgroundTasks,
    db_conn = Depends(db.get_db_connection),
    client : httpx.AsyncClient = Depends(get_http_client)
):
    """
    Fetches the RSS feeds for all subscribed YouTube channels,
    generates the summary, and stores it in the DB.
    """
    channel_ids = await subscription_management.get_subscription_ids(db_conn)
    task_id = uuid.uuid4()
    # background_tasks.add_task(write_notification, email, message="some notification")
    await asyncio.gather(
        *[ingest_rss_feed(
            session = client,
            db_conn = db_conn,
            channel_id = channel_id
        ) for channel_id in channel_ids]
    )

@router.get("/list_subscriptions")
async def list_subscriptions(
    db_conn = Depends(db.get_db_connection)
):
    """
    Returns all the YouTube channels that are subscribed to
    """
    return await subscription_management.list_all_subscription_details(
        db_conn
    )
    

@router.delete("/remove_subscriptions")
async def remove_subscription(
    channel_id : str,
    db_conn = Depends(db.get_db_connection)
):
    """
    Remove a subscription for a YouTube channel
    """
    return await subscription_management.remove_subscription(
        db_conn,
        channel_id
    )

@router.get("/get_channel_details")
async def get_channel_details(channel_id : str):
    """
    An endpoint to get the details of a channel
    """
    pass

@router.get("/get_channel_videos")
async def get_channel_videos(channel_id : str):
    """
    An endpoint to get the videos of a channel
    """
    pass
