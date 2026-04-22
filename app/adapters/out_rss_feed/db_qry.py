"""
The following code are the queries used by the output RSS feed code
to generate a RSS feed from the items in the database.

References
 - https://www.rssboard.org/rss-specification#requiredChannelElements
 - https://www.rssboard.org/rss-specification#hrelementsOfLtitemgt

"""
import asyncio
import textwrap

import aiosqlite
from loguru import logger

from . import model

async def get_channel(conn: aiosqlite.Connection, channel_id: str) -> model.DB_Channel:
    """
    Get a specific channel subscription by ID.

    Example usage:
        async with get_db_connection() as conn:
            subscription = await get
            channel(conn, 'UC2DjFE7Xf11URZqWBigcVOQ')
    """
    cursor = await conn.execute("""
        SELECT channel_id, channel_name, channel_description
        FROM subscriptions WHERE channel_id=? ORDER BY created_at DESC
    """, (channel_id,))
    row = await cursor.fetchone()
    if not row:
        raise Exception(f"Channel with ID {channel_id} not found")
    return model.DB_Channel(**dict(row))

async def get_channel_header(channel: model.DB_Channel) -> str:
    """
    Get the RSS feed header for a given channel.
    """
    return textwrap.dedent(f"""
        <title>{channel.title}</title>
        <link>{channel.link}"</link>
        <description>{channel.description}</description>
        """).strip()



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
        SELECT video_name, date_published, url, thumbnail, article
        FROM videos
        WHERE channel_name == (
            SELECT channel_name
            FROM subscriptions
            WHERE channel_id = ? ORDER BY created_at DESC LIMIT 1
        ) AND date_published > datetime('now', '-30 days')
    """, (channel_id,))
    rows = await cursor.fetchall()
    return [model.DB_Item(**dict(row)) for row in rows]

async def get_items_str(items: list[model.DB_Item]) -> str:
    """
    Get the RSS feed headers for a given list of items.
    """
    return "\n".join([
        textwrap.dedent(f"""
            <item>
                <title>{item.title}</title>
                <link>{item.link}</link>
                <description>{item.description[:100]}...</description>
                <content:encoded>{item.description}</content:encoded>
                <media:thumbnail url="{item.thumbnail}"/>
                <pubDate>{item.date_published}</pubDate>
            </item>
        """).strip()
    for item in items])

async def get_rss_feed_str(channel: model.DB_Channel, items: list[model.DB_Item]) -> str:
    """
    Get the complete RSS feed as a string.
    """
    return textwrap.dedent(f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
          <channel>
            {await get_channel_header(channel)}
            {await get_items_str(items)}
          </channel>
        </rss>
    """).strip()

async def get_rss_feed(conn: aiosqlite.Connection, channel_id: str) -> str:
    """
    Get the complete RSS feed as a string for a specific channel.
    """
    results = await asyncio.gather(
        get_channel(conn, channel_id),
        get_items(conn, channel_id)
    )
    channel, items = results
    logger.info(f"Channel {channel.channel_id} -> {channel.channel_name}")
    return await get_rss_feed_str(channel, items)