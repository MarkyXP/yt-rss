import aiosqlite
from . import model


async def get_all_channels(conn: aiosqlite.Connection) -> list[model.DB_Channel]:
    """
    Get all channel subscriptions.
    
    Example usage:
        async with get_db_connection() as conn:
            subscriptions = await get_subscriptions(conn)
    
    Returns:
        List of dictionaries with subscription data.
    """
    cursor = await conn.execute("""
        SELECT channel_id, channel_name
        FROM subscriptions ORDER BY created_at DESC
    """)
    rows = await cursor.fetchall()
    return [model.DB_Channel(**dict(row)) for row in rows]

async def get_channel(conn: aiosqlite.Connection, channel_id: str) -> model.DB_Channel:
    """
    Get a specific channel subscription by ID.

    Example usage:
        async with get_db_connection() as conn:
            subscription = await get
            channel(conn, 'UC2DjFE7Xf11URZqWBigcVOQ')
    """
    cursor = await conn.execute("""
        SELECT channel_id, channel_name
        FROM subscriptions WHERE channel_id=? ORDER BY created_at DESC
    """, (channel_id,))
    row = await cursor.fetchone()
    if not row:
        raise Exception(f"Channel with ID {channel_id} not found")
    return model.DB_Channel(**dict(row))

async def get_items(conn: aiosqlite.Connection, channel_id: str) -> list[model.DB_Item]:
    """
    Get all recent items from a specific channel subscription.

    Args:
        conn : The database connection object.
        channel_id : The YouTube channel ID.

    Returns:
        A list of DB_Item objects containing the video name, date published,
        URL, and article text.
    """
    cursor = await conn.execute("""
        SELECT video_name, date_published, url, article
        FROM videos
        WHERE channel_name == (
            SELECT channel_name
            FROM subscriptions
            WHERE channel_id=? ORDER BY created_at DESC LIMIT 1
        ) AND date_published > datetime('now', '-30 days')
    """, (channel_id,))
    rows = await cursor.fetchall()
    return [model.DB_Item(**dict(row)) for row in rows]