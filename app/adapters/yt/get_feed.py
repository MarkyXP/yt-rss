"""
A custom written interface to

https://www.reddit.com/r/rss/comments/1n1hbsb/ive_built_a_simple_tool_for_getting_youtube_rss/
https://www.newskeeper.io/tools/youtube-rss

"""

import re

import httpx
import xmltodict
from lxml import etree

from .model_feed import Feed

_channel_id_pattern = re.compile(r"channel_id=([a-zA-Z0-9]*)")


async def get_channel_id(session: httpx.AsyncClient, channel_name: str) -> str:
    """
    Takes the channel's name (e.g. eevblog) or its link (e.g. https://www.youtube.com/eevblog)
    and returns the channel ID (e.g. UC2DjFE7Xf11URZqWBigcVOQ)

    Args:
        session (httpx.AsyncClient): The HTTP session to use.
        channel_name (str) : The Youtube channel's name (e.g. eevblog) or its link (e.g. https://www.youtube.com/eevblog)

    Returns:
        str : The channel ID of the given channel (e.g. UC2DjFE7Xf11URZqWBigcVOQ)

    Usage:
        >>> asyncio.run(
        ...     get_channel_id(
        ...         httpx.AsyncClient(),
        ...         "eevblog"
        ...     )
        ... )  # doctest: +SKIP
        'UC2DjFE7Xf11URZqWBigcVOQ'

        >>> asyncio.run(get_channel_id("markisthebest")) # doctest: +SKIP
        Traceback (most recent call last):
        ...
        ValueError: The number must be non-negative.
    """
    if not channel_name.startswith("https://"):
        channel_name = f"https://www.youtube.com/{channel_name}"
    response = await session.get(channel_name)
    response.raise_for_status()
    matches = _channel_id_pattern.findall(response.text)
    if not matches:
        raise ValueError(f"Could not find channel ID for {channel_name}")
    return matches[0]


async def get_rss_feed(session: httpx.AsyncClient, channel_id: str) -> Feed:
    """
    Fetch the RSS feed of a YouTube channel.

    Args:
        session (httpx.AsyncClient): The HTTP session to use.
        channel_id (str): The ID of the YouTube channel.

    Returns:
        dict: The RSS feed

    Usage:
        >>> asyncio.run(
        ...     get_rss_feed(
        ...         session = httpx.AsyncClient(),
        ...         channel_id = "UC2DjFE7Xf11URZqWBigcVOQ"
        ...     )
        ... ).id
        '2DjFE7Xf11URZqWBigcVOQ'
    """
    url = f"https://www.youtube.com/feeds/videos.xml"
    params = {
        "channel_id" : channel_id
    }
    response = await session.get(url, params = params)
    response.raise_for_status()
    root = etree.fromstring(response.content)
    xml_dict = xmltodict.parse(etree.tostring(root))
    feed = Feed(xml_dict['feed'])
    return feed


if __name__ == "__main__":
    import asyncio
    import doctest
    doctest.testmod(
        optionflags= doctest.ELLIPSIS
    )