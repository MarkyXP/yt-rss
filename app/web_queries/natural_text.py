"""
#==============================================================================
# ** Natural Text
#-----------------------------------------------------------------------------
#  @Author: Mark Evans
#  @Date:   2025-Nov-27
#-----------------------------------------------------------------------------
#  This web query calls a Large Language Model (LLM) such as OpenAI, Groq,
#  or Gemini to analyse the YouTube transcript and either:
#   * generate a summary article, or 
#   * generate tags for the transcript.
#==============================================================================
"""
import typing

import httpx

from app.core.config import CONFIG
from app.core.user_settings import SETTINGS

async def _query_llm(
        client : httpx.AsyncClient,
        messages : typing.List[typing.Dict[str, str]],
        temperature : int = 0.7,
        max_tokens : int = 800
) -> str:
    """
    Calls the LLM with the query provided, detects and raises any errors, 
    otherwise returns the text from the LLM
    """
    resp = await client.post(
        url = SETTINGS.LLM_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SETTINGS.LLM_API_KEY}"
        },
        json={
            "model": SETTINGS.LLM_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
    )
    jResp = resp.json()
    if resp.status_code != 200:
        raise AssertionError(resp.content)
    if "error" in jResp:
        raise ValueError(jResp["error"]["message"])
    content = jResp["choices"][0]["message"]["content"]
    return content


async def generate_article(client : httpx.AsyncClient, transcript: str):
    """
    Uses a large language model to take a YouTube transcript
    and returns an SEO article.

    Usage:
        >>> asyncio.run(
        ...     generate_article(
        ...         httpx.AsyncClient(),
        ...         "yt-rss generates a RSS feed for your favourite youtubers!"
        ...     )
        ... )
        '...'
    """
    _prompt = CONFIG.PROMPTS.GENERATE_ARTICLE.get_sys_prompt()
    messages = [
        {
            "role": "system",
            "content": _prompt,
        },
        {"role": "user", "content": f"Transcript: {transcript}"},
    ]
    article = await _query_llm(client, messages)
    return article


async def generate_tags(client : httpx.AsyncClient, transcript: str):
    """
    Uses a large language model to generate tags for a transcript
    so users can elect to skip a video if they want
    """
    pass


if __name__ == "__main__":
    import asyncio
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)