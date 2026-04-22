"""
The interactions with the YouTube channels

References:
|            |   |
|------------|---|
| Decorators | https://medium.com/django-unleashed/python-decorators-the-three-layer-pattern-449406659e5c |
| Line Profiling | https://python.plainenglish.io/profiling-performance-in-python-step-by-step-guide-9d9625c56b32 |
"""

import asyncio
import collections
import uuid_utils as uuid
import functools
import time
import traceback

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from loguru import logger

from app.db import db
from app.workflow.index import index_rss_feed
from app.workflow import subscription_management

import httpx

background_task_list = {}

# @asynccontextmanager
async def get_http_client():# -> asyncio.AsyncGenerator[httpx.AsyncClient]:
    """
    An asynchronous dependency that provides an httpx.AsyncClient.

    The client is created within an async context manager (async with), 
    ensuring it is properly closed when the request is done.
    """
    async with httpx.AsyncClient() as client:
        yield client


def rate_limiter(rate_limits : dict[int, int]):
    """
    Adds a rate limit to the wrapped function for how frequently the wrapped
    function can be called.

    Args:
        - rate_limits (dict[int, int]): A dictionary of {number of queries allowed: time limit (seconds)}
           e.g. {5: 60} would allow 5 queries in 60 seconds.
    """
    def decorator(function):
        # The persistent variables that will be used to keep track
        num_queries_to_remember = max(list(rate_limits.keys()))
        all_previous_run_times = collections.defaultdict(
            lambda: collections.deque(
                [0]*num_queries_to_remember,
                maxlen=num_queries_to_remember
            )
        )
        @functools.wraps(function)
        async def wrapper(request: Request, *args, **kwargs):
            # Get the query source (e.g. IP address) of the request and lookup its query history.
            query_src = request.client.host
            now = int(time.monotonic())
            previous_run_times = all_previous_run_times[query_src]
            # For each query limit (e.g. the 5 query limit, the 10 query limit)
            for query_count_limit in rate_limits:
                # Calculate the time since the las
                min_interval_time = rate_limits[query_count_limit]
                d_time = now - previous_run_times[query_count_limit-2]
                if d_time < min_interval_time:
                    retry_secs = min_interval_time - d_time
                    raise HTTPException(
                        status_code = 429,
                        detail = f"Please try again in {retry_secs} seconds"
                    )
            previous_run_times.appendleft(now)
            return await function(request, *args, **kwargs)
        return wrapper
    return decorator


router = APIRouter()

@router.post("/add_subscription")
# Limit to 3 subscriptions in 5 minutes, or 10 subscriptionsper day
@rate_limiter({3 : 600, 10 : 86400})
async def add_subscription(
    request : Request,
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

async def _background_update_channels(task_id : str, channel_ids : list[str]) -> None:
    global background_task_list
    logger.info(f"Starting update task {task_id} for channels {', '.join(channel_ids)}")
    background_task_list[task_id] = f"Running update for channels {', '.join(channel_ids)}"
    try:
        async with httpx.AsyncClient() as client:
            async for db_conn in db.get_db_connection():
                await asyncio.gather(
                    *[index_rss_feed(
                        session = client,
                        db_conn = db_conn,
                        channel_id = channel_id
                    ) for channel_id in channel_ids]
                )
        background_task_list[task_id] = f"Complete"
    except Exception as e:
        logger.error(f"Error updating channels {', '.join(channel_ids)}: {e}")
        background_task_list[task_id] = f"Failed - {traceback.format_exc()}"

# @router.post("/update_channels")
async def update_channels(
    channel_ids : list[str] | None = None,
    db_conn = Depends(db.get_db_connection),
    client : httpx.AsyncClient = Depends(get_http_client)
):
    await asyncio.gather(
        *[index_rss_feed(
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
    
    global background_task_list
    channel_ids = await subscription_management.get_subscription_ids(db_conn)
    task_id = str(uuid.uuid6())
    background_tasks.add_task(
        _background_update_channels,
        task_id = task_id,
        channel_ids = channel_ids
    )
    return task_id

@router.get("/get_update_status/{task_id}")
async def get_update_status(task_id: str):
    global background_task_list
    status = background_task_list.get(task_id, "Error")
    if status == "Error":
        raise HTTPException(status_code=404, detail=f"Task id {task_id} not found.")
    if status == "Complete":
        background_task_list.pop(task_id)
    return status

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

# @router.get("/get_channel_details")
async def get_channel_details(channel_id : str):
    """
    An endpoint to get the details of a channel
    """
    pass

# @router.get("/get_channel_videos")
async def get_channel_videos(channel_id : str):
    """
    An endpoint to get the videos of a channel
    """
    pass
