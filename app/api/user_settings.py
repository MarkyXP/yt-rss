import typing

import httpx
from fastapi import APIRouter, Depends, Query

from app.db import user_settings
from app.db import db
from app.web_queries import web

router = APIRouter()


@router.put("/add_channel")
async def add_channel(
    channel_handle: str, db=Depends(db.get_session), client=Depends(web.get_client)
):
    channel_id = await user_settings.add_channel(channel_handle, db, client)
    if channel_id > 0:
        return {"status": "ok", "channel_handle": channel_handle, "channel_id": channel_id}
    return {"status": "bad", "msg" : f"Error adding channel {channel_handle} to the database.\nConfirm the handle is correct, and it's not already in the database"}


@router.get("/list_channels")
async def list_channels(
    offset: int = 0,
    limit: typing.Annotated[int, Query(le=100)] = 100,
    db=Depends(db.get_session),
):
    channels = await user_settings.list_channels(offset, limit, db)
    return {"status": "ok", "channels": channels}


@router.delete("/remove_channel")
def remove_channel(channel_id: int, db=Depends(db.get_session)):
    user_settings.remove_channel(channel_id, db)
    return {"status": "ok", "message": f"Successfully removed channel ID {channel_id}"}
