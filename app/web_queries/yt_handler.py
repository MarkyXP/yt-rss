import asyncio
import dataclasses
import functools
import typing

import httpx
from ytfetcher import YTFetcher

from app.web_queries.natural_text import generate_article


@dataclasses.dataclass
class VideoSummary:
    title: str
    description: str
    url: str
    channel: str
    duration: str
    duration_seconds: int
    thumbnail: str
    transcript: str

    @functools.lru_cache
    def body(self):
        article = generate_article(self.transcript)
        return article


async def get_videos(
    channel_handle: str, no_videos: int
) -> typing.AsyncGenerator[VideoSummary]:
    fetcher = YTFetcher.from_channel(
        channel_handle=channel_handle, max_results=no_videos
    )
    channel_data = await fetcher.fetch_youtube_data()
    for video in channel_data:
        transcript = " ".join(t.text for t in video.transcripts)
        mins = int(video.metadata.duration / 60)
        secs = int(video.metadata.duration % 60)
        duration_str = f"{mins}:{secs:02}"
        video_summary = VideoSummary(
            title=video.metadata.title,
            description=video.metadata.description,
            url=video.metadata.url,
            channel=channel_handle,
            duration=duration_str,
            duration_seconds=video.metadata.duration,
            thumbnail=video.metadata.thumbnails[-1]["url"],
            transcript=transcript,
        )
        yield video_summary


async def check_channel_exists(
    channel_handle: str, web_client: httpx.AsyncClient
) -> bool:
    """
    Checks if f"https://www.youtube.com/@{channel_handle}" exists.
    Returns True if it exists, False if it gets a 404 error
    """
    response = await web_client.get(f"https://www.youtube.com/@{channel_handle}")
    return response.status_code == 200
