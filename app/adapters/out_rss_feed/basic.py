"""

 - https://www.rssboard.org/rss-specification#requiredChannelElements
 - https://www.rssboard.org/rss-specification#hrelementsOfLtitemgt

"""
import asyncio
import textwrap

import aiosqlite
from loguru import logger

from . import db_qry, model

async def get_channel_header(channel: model.DB_Channel) -> str:
    """
    Get the RSS feed header for a given channel.
    """
    return textwrap.dedent(f"""
        <title>{channel.title}</title>
        <link rel="self" href="{channel.link}"/>
        <description></description>
        """).strip()

async def get_items_str(items: list[model.DB_Item]) -> str:
    """
    Get the RSS feed headers for a given list of items.
    """
    return "\n".join([
        textwrap.dedent(f"""
            <item>
                <title>{item.title}</title>
                <link rel="alternate" href="{item.link}"/>
                <description>{item.article}</description>
                <pubDate>{item.date_published}</pubDate>
            </item>
        """).strip()
    for item in items])

async def get_rss_feed_str(channel: model.DB_Channel, items: list[model.DB_Item]) -> str:
    """
    Get the complete RSS feed as a string.
    """
    return textwrap.dedent(f"""
        <channel>
        {await get_channel_header(channel)}
        {await get_items_str(items)}
        </channel>
    """).strip()

async def get_rss_feed(conn: aiosqlite.Connection, channel_id: str) -> str:
    """
    Get the complete RSS feed as a string for a specific channel.
    """
    results = await asyncio.gather(
        db_qry.get_channel(conn, channel_id),
        db_qry.get_items(conn, channel_id)
    )
    channel, items = results
    logger.info(f"Channel {channel.channel_id} -> {channel.channel_name}")
    return await get_rss_feed_str(channel, items)