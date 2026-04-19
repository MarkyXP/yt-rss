
from fastapi import APIRouter, Depends, Response
from loguru import logger

from app.db import db

from . import db_qry

router = APIRouter()

@router.get("/get_feed/{channel_id}")
async def get_feed(
    channel_id: str,
    db_conn = Depends(db.get_db_connection)
):
    logger.info(f"Requested RSS feed for {channel_id}")
    feed = await db_qry.get_rss_feed(db_conn, channel_id)
    return Response(content=feed, media_type="text/xml")
