import asyncio
import time

import httpx
from loguru import logger

from app.api import subscriptions
from app.core.config import CONFIG

async def bg_run_update():
    """
    Calls the app.api.channels.update_all_subscribed_channels function
    every UPDATE_INTERVAL_MINS minutes.
    """
    while True:
        # Fetch the YouTube videos for each subscribed channel & update the database
        start_time = time.time()
        async for db in subscriptions.db.get_db_connection():
            async with httpx.AsyncClient() as client:
                logger.info("Beginning background task to update all channels...")
                await subscriptions.update_all_subscribed_channels(
                    db_conn=db,
                    client = client
                )
        # Calculate when this should run next
        end_time = time.time()
        time_to_next_run = CONFIG.UPDATE_INTERVAL_MINS * 60 - (end_time - start_time)
        # Sleep until the next update interval
        await asyncio.sleep(max(time_to_next_run, 0))