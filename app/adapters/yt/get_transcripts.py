"""
## Download the transcripts from YouTube for a given video URL.


"""
import asyncio
import html

import httpx
from loguru import logger

from app.core.config import CONFIG

_SEM = asyncio.Semaphore(1)

async def get_transcript(client : httpx.AsyncClient, video_url : str) -> str:
    """Download the transcripts from YouTube for a given video URL.

    Args:
        - client (httpx.AsyncClient): The HTTP client to use for the request.
        - video_url (str): The URL of the video to download the transcripts for.

    Returns:
        str: The transcripts for the video.

    Usage:
        >>> asyncio.run(
        ...     get_transcripts(
        ...         httpx.AsyncClient(),
        ...         "https://www.youtube.com/watch?v=aFPghfjgqAQ&pp=ygUNYXJ0aXNhbiBtYWtlcw%3D%3D"
        ...     )
        ... )
        "Now, I'm sure you all know that I love me a good cordless drill..."
    """
    async with _SEM:
        logger.info(f"Fetching transcripts from {video_url}...")
        resp = await client.get(
            url = CONFIG.TRANSCRIPTION_BASE_URL,
            params = {"url" : video_url},
            timeout = 20 # Took ~7sec during dev testing
        )
        logger.info("\tTranscript fetched. Analyzing...")
    resp.raise_for_status()
    jResp = resp.json()
    try:
        text = ' '.join([
            html.unescape(
                str(chunk["text"])
            ) for chunk in jResp["transcript"]
        ])
    except:
        text = 'No transcript found.'
    logger.info(f"\tTranscript: {text[:30]}...")
    return text

if __name__ == "__main__":
    import asyncio
    import doctest
    doctest.testmod(
        optionflags=doctest.ELLIPSIS,
        verbose=True# , extraglobs={"client": httpx.AsyncClient()}
    )