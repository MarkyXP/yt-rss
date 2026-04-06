import textwrap

import httpx
from loguru import logger

from app.adapters.yt.model_feed import Entry
from app.core.config import CONFIG

with open("app/adapters/summarizer/prompt.llm", "r") as f:
    _SUMMARY_SYS_PROMPT = f.read()

async def chat_llm(
        session : httpx.AsyncClient,
        messages : list[str],
        sys_prompt : str = _SUMMARY_SYS_PROMPT.strip()
) -> str:
    """
    chats to Jimmy Chat AI

    Args:
       session (httpx.AsyncClient): The HTTP session to use for making requests.
       video_data (dict): A dictionary containing the video data, including the title, author, and captions
    
    Returns:
        str: A summary of the video

    Usage:
        >>> asyncio.run(
        ...     chat_llm(
        ...         session = httpx.AsyncClient(),
        ...         messages = ["Hello"],
        ...         sys_prompt = ""
        ...     )
        ... ).upper()
        '...HELLO...'
    """
    url = CONFIG.LLM_BASE_URL
    json = {
        "messages":[
            {
                "role" : "user",
                "content" : message
            }
            for message in messages
        ],
        "chatOptions":{
            "selectedModel": CONFIG.LLM_MODEL_NAME,
            "systemPrompt": sys_prompt,
            "topK": 2
        },
        "attachment":None
    }
    resp = await session.post(url = url, json = json)
    resp.raise_for_status()
    summary = resp.text
    if '<|stats|>' in summary:
        summary = summary.split('<|stats|>')[0].strip()
    return str(summary)

async def get_summary(
        session : httpx.AsyncClient,
        video_data : Entry,
        transcript : str
) -> str:
    """
    Generates a summary of a YouTube video using the Jimmy Chat

    Args:
       session (httpx.AsyncClient): The HTTP session to use for making requests.
       video_data (dict): A dictionary containing the video data, including the title, author, and captions
    
    Returns:
        str: A summary of the video

    Usage:
        >>> asyncio.run(
        ...     get_summary(
        ...         session = httpx.AsyncClient(),
        ...         video_data = {
        ...             "author": "EEVblog",
        ...             "title": "EEVblog 1735 - Power Rail Probing & Oscilloscope DC Offset EXPLAINED",
        ...             "captions": open("app/adapters/summarizer/example_captions.txt", "r").read()
        ...         }
        ...     )
        ... )
        '...'
    """
    video_data_str = textwrap.dedent(f"""
        [VIDEO DETAILS]
        Video Author: {video_data.author.name},
        Video Title: {video_data.title},
        Video Captions: {transcript}
        [/VIDEO DETAILS]
        Please provide the summary of the _ABOVE_ video details.
    """).strip()
    logger.info(f"Getting Summary of video: '{video_data.title}'")
    summary = await chat_llm(
        session,
        [video_data_str[:20_000]]
    )
    logger.info(f"\tSummary of '{video_data.title}'\t{summary[:100]}...")
    return summary

if __name__ == "__main__":
    import asyncio
    import doctest
    doctest.testmod(
        verbose = True,
        optionflags = doctest.ELLIPSIS
    )