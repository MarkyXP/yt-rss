import asyncio
import httpx
import aiosqlite

from app.db import db
from app.adapters import yt

async def add_subscription(
        session : httpx.AsyncClient,
        db_conn : aiosqlite.Connection,
        channel_name : str,
):
    """
    Fetches the YouTube channels ID, and adds it to the database
    for ongoing subscription scraping

    Args:
        - session (httpx.AsyncClient): The HTTP client used to make requests.
        - db_conn (aiosqlite.Connection): The connection to the SQLite database.
        - channel_name (str): The name of channel_name (str) : The Youtube channel's name (e.g. eevblog) or its link (e.g. https://www.youtube.com/eevblog)
    
    Returns:
        - Channel ID (str): The YouTube channel (e.g. 'UC2DjFE7Xf11URZqWBigcVOQ')
    """
    # Strip the https://youtube.com/
    channel_name = channel_name.lower().replace("https://www.youtube.com/", "")
    channel_id = await yt.get_channel_id(session, channel_name)
    db_index = await db.add_subscription(
        conn = db_conn,
        channel_id = channel_id.id,
        channel_name = channel_id.name
    )
    return channel_id.id

async def get_subscription_ids(
        db_conn : aiosqlite.Connection
):
    """
    Gets the subscription IDs from the database.

    Args:
        - db_conn (aiosqlite.Connection): The connection to the SQLite database.

    Returns:
        - list[str] : A list of subscription IDs (e.g. ['UC2DjFE7Xf11URZqWBigcVOQ'])
    """
    subscriptions = await db.get_subscriptions(db_conn)
    ids = [sub['channel_id'] for sub in subscriptions]
    return ids

async def list_all_subscription_details(
        db_conn : aiosqlite.Connection
):
    """
    Gets the subscription details from the database

    Args:
        - db_conn (aiosqlite.Connection): The connection to the SQLite database.

    Returns:
        - list[dict]: A list of dictionaries containing the details of each subscription
        ```
            [
                {
                    "id" : 1,
                    "channel_id" : "UC2DjFE7Xf11URZqWBigcVOQ"
                    "channel_name" : "eevblog",
                    "created_at" : "2026-03-30 12:17:29"
                }, ...
            ]
        ```
    """
    subscriptions = await db.get_subscriptions(db_conn)
    return subscriptions

async def remove_subscription(
        db_conn : aiosqlite.Connection,
        channel_id : str
) -> bool:
    """
    Drops a subscription from the database.

    Args:
        - db_conn (aiosqlite.Connection): The connection to the SQLite database.
        - channel_id (str): The ID of the channel to be removed.

    Returns:
        - bool: True if the subscription was successfully removed, False otherwise.
    """
    count_dropped = await db.remove_subscription(
        db_conn,
        channel_id
    )
    return count_dropped