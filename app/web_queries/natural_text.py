import asyncio

from groq import AsyncGroq

from app.core.config import CONFIG

_prompt = CONFIG.PROMPTS.GENERATE_ARTICLE.get_sys_prompt()
_client = AsyncGroq(
    api_key=CONFIG.GROQ_API_KEY,
)


async def generate_article(transcript: str):
    """
    Uses a large language model to take a YouTube transcript
    and returns an SEO article.

    Usage:
        >>> asyncio.run(
            generate_article(
                "yt-rss generates a RSS feed for your favourite youtubers!"
            )
        )
        '...'
    """
    chat_completion = await _client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": _prompt,
            },
            {"role": "user", "content": f"Transcript: {transcript}"},
        ],
        model=CONFIG.GROQ_MODEL,
    )
    body = chat_completion.choices[0].message.content
    return body


def generate_tags(transcript: str):
    """
    Uses a large language model to generate tags for a transcript
    so users can elect to skip a video if they want
    """
    pass


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
