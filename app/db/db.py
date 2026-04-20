"""
Database module for storing and retrieving YouTube video information.

Example usage:
    async with get_db_connection() as conn:
        cursor = await conn.execute("SELECT * FROM videos WHERE channel_name = ?", (channel_name,))
        rows = await cursor.fetchall()
        videos = [dict(row) for row in rows]
"""

import aiosqlite
import html
from typing import List, Optional, Dict, Any, AsyncGenerator
from pathlib import Path
from contextlib import asynccontextmanager

from loguru import logger

from app.core.config import CONFIG

# Database file path
DB_PATH = Path(CONFIG.DB_LOCATION)
# Create the directory and any missing parents
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# @asynccontextmanager
async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection]:
    """
    Get a database connection.
    
    Example usage:
        async with get_db_connection() as conn:
            cursor = await conn.execute("SELECT * FROM videos")
            rows = await cursor.fetchall()
            videos = [dict(row) for row in rows]
    """
    #logger.info("Creating database connection")
    conn = await aiosqlite.connect(DB_PATH)
    await conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = aiosqlite.Row
    try:
        yield conn
    finally:
        await conn.close()
        #logger.info("Database connection closed")

async def init_db() -> None:
    """Initialize the database with required tables."""
    async for conn in get_db_connection():
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_name TEXT NOT NULL,
                video_name TEXT NOT NULL,
                date_published TEXT,
                url TEXT UNIQUE NOT NULL,
                thumbnail TEXT,
                transcript TEXT,
                article TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT UNIQUE NOT NULL,
                channel_name TEXT NOT NULL,
                channel_description TEXT NOT NULL,
                channel_thumbnail TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await conn.commit()


async def add_video(
    conn: aiosqlite.Connection,
    channel_name: str,
    video_name: str,
    date_published: Optional[str] = None,
    url: str = "",
    thumbnail: Optional[str] = None,
    transcript: Optional[str] = None,
    article: Optional[str] = None,
) -> int:
    """
    Add a YouTube video to the database.
    
    Example usage:
        async with get_db_connection() as conn:
            video_id = await add_video(
                conn=conn,
                channel_name="Test Channel",
                video_name="Test Video",
                url="https://www.youtube.com/watch?v=test123"
            )
    
    Returns:
        The ID of the inserted video.
    """
    logger.info(f"Adding video to database: {channel_name} - {video_name}")
    query = """
        INSERT OR IGNORE INTO videos 
        (channel_name, video_name, date_published, url, thumbnail, transcript, article)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    args = (
        html.unescape(channel_name),
        html.unescape(video_name),
        html.unescape(date_published),
        html.unescape(url),
        html.unescape(thumbnail),
        html.unescape(transcript),
        html.unescape(article),
    )
    try:
        cursor = await conn.execute(query, args)
        await conn.commit()
        logger.info(f"\tvideo added to database: {channel_name} - {video_name}")
        return cursor.lastrowid
    except Exception as e:
        logger.error(e)


async def get_video_by_url(conn: aiosqlite.Connection, url: str) -> Optional[Dict[str, Any]]:
    """
    Get a video by its URL.
    
    Example usage:
        async with get_db_connection() as conn:
            video = await get_video_by_url(conn, "https://www.youtube.com/watch?v=test123")
    
    Returns:
        Dictionary with video data or None if not found.
    """
    cursor = await conn.execute(
        "SELECT * FROM videos WHERE url = ?", (url,)
    )
    row = await cursor.fetchone()
    return dict(row) if row else None


async def get_videos_by_channel(conn: aiosqlite.Connection, channel_name: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get videos by channel name.
    
    Example usage:
        async with get_db_connection() as conn:
            videos = await get_videos_by_channel(conn, "Test Channel", limit=50)
    
    Returns:
        List of dictionaries with video data.
    """
    cursor = await conn.execute(
        "SELECT * FROM videos WHERE channel_name = ? ORDER BY date_published DESC LIMIT ?",
        (channel_name, limit),
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def get_all_videos(conn: aiosqlite.Connection, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get all videos from the database.
    
    Example usage:
        async with get_db_connection() as conn:
            all_videos = await get_all_videos(conn, limit=100)
    
    Returns:
        List of dictionaries with video data.
    """
    cursor = await conn.execute(
        "SELECT * FROM videos ORDER BY updated_at DESC LIMIT ?", (limit,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def update_video_transcript(conn: aiosqlite.Connection, url: str, transcript: str) -> bool:
    """
    Update a video's transcript.
    
    Example usage:
        async with get_db_connection() as conn:
            updated = await update_video_transcript(conn, "https://www.youtube.com/watch?v=test123", "New transcript")
    
    Returns:
        True if updated, False if video not found.
    """
    cursor = await conn.execute(
        """
        UPDATE videos 
        SET transcript = ?, updated_at = CURRENT_TIMESTAMP
        WHERE url = ?
        """,
        (transcript, url),
    )
    await conn.commit()
    return cursor.rowcount > 0


async def update_video_article(conn: aiosqlite.Connection, url: str, article: str) -> bool:
    """
    Update a video's article/summary.
    
    Example usage:
        async with get_db_connection() as conn:
            updated = await update_video_article(conn, "https://www.youtube.com/watch?v=test123", "New article")
    
    Returns:
        True if updated, False if video not found.
    """
    cursor = await conn.execute(
        """
        UPDATE videos 
        SET article = ?, updated_at = CURRENT_TIMESTAMP
        WHERE url = ?
        """,
        (article, url),
    )
    await conn.commit()
    return cursor.rowcount > 0


async def add_subscription(
        conn: aiosqlite.Connection,
        channel_id: str,
        channel_name: str,
        channel_description : str,
        channel_thumbnail : str
) -> int:
    """
    Add a channel subscription to the database.
    
    Example usage:
        async with get_db_connection() as conn:
            subscription_id = await add_subscription(conn, "UC123456789", "Test Channel", "Wow, what an amazing channel!", "https://i.imgur.com/123456789.jpg")
    
    Returns:
        The ID of the inserted subscription.
    """
    cursor = await conn.execute(
        """
        INSERT OR IGNORE INTO subscriptions 
        (channel_id, channel_name, channel_description, channel_thumbnail)
        VALUES (?, ?, ?, ?)
        """,
        (
            html.unescape(channel_id),
            html.unescape(channel_name),
            html.unescape(channel_description),
            channel_thumbnail
        ),
    )
    await conn.commit()
    return cursor.lastrowid


async def get_subscriptions(conn: aiosqlite.Connection) -> List[Dict[str, Any]]:
    """
    Get all channel subscriptions.
    
    Example usage:
        async with get_db_connection() as conn:
            subscriptions = await get_subscriptions(conn)
    
    Returns:
        List of dictionaries with subscription data.
    """
    cursor = await conn.execute("SELECT * FROM subscriptions ORDER BY created_at DESC")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def remove_subscription(conn: aiosqlite.Connection, channel_id: str) -> bool:
    """
    Remove a channel subscription.
    
    Example usage:
        async with get_db_connection() as conn:
            removed = await remove_subscription(conn, "UC123456789")
    
    Returns:
        True if removed, False if not found.
    """
    cursor = await conn.execute(
        "DELETE FROM subscriptions WHERE channel_id = ?", (channel_id,)
    )
    await conn.commit()
    return cursor.rowcount > 0
