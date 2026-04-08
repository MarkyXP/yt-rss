import asyncio
import traceback

import aiosqlite
import httpx
from loguru import logger

from app.adapters.summarizer.summarizer_1 import get_summary
from app.adapters.yt import get_rss_feed, get_transcript, Entry
from app.db import db
from app.workflow import subscription_management


async def _ingest_video(
        session : httpx.AsyncClient,
        db_conn : aiosqlite.Connection,
        video : Entry
):
    """Ingests a specific YouTube _VIDEO_"""
    # Skip the video if it's a short
    if '/shorts/' in video.href:
        return
    # Skip if the database exists
    if await db.get_video_by_url(db_conn, video.href) is not None:
        return
    # Get the transcripts
    transcript = await get_transcript(session, video.href)
    # Get the LLM Summary
    summary = await get_summary(session, video, transcript)
    # Add it to the datbase
    await db.add_video(
        conn = db_conn,
        channel_name = video.author.name,
        video_name = video.title,
        date_published = video.published,
        url = video.href,
        thumbnail = video.thumbnail,
        transcript = transcript,
        article = summary
    )
    

async def ingest_rss_feed(
    session : httpx.AsyncClient,
    db_conn : aiosqlite.Connection,
    channel_id : str
):
    """
    Ingests the data for a given YouTube _CHANNEL_.
    """
    # channel_ids = await subscription_management.get_subscription_ids(db_conn)
    logger.info(f"Ingesting the RSS feed for {channel_id}")
    feed = await get_rss_feed(session, channel_id)
    await asyncio.gather(
        *[
            _ingest_video(session, db_conn, entry)
            for entry in feed.entries
        ]
    )
    logger.info(f"Ingestion successfully complete for {channel_id}")

if __name__ == "__main__":
    async def main():
        channel_ids = ["UC2DjFE7Xf11URZqWBigcVOQ", "UCtM5z2gkrGRuWd0JQMx76qA"]
        async with httpx.AsyncClient() as session:
            async for db_conn in db.get_db_connection():
                results = await asyncio.gather(
                    *[ingest_rss_feed(
                        session,
                        db_conn,
                        channel_id
                    ) for channel_id in channel_ids],
                    return_exceptions=True
                )
                for r in results:
                    if isinstance(r, Exception):
                        print(f"Task failed: {r}")
                await db_conn.commit()
    
    asyncio.run(main())
