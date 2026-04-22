import re

_BOLD_PATTERN = re.compile(r"(\*\*)+")

def format_llm_resp(text : str) -> str:
    """
    Converts the LLM response (usually Markdown format) into
    a format used by the RSS feeds (html)
    """
    out = ""
    for line in text.split("\n"):
        # Skip empty lines
        if not line.strip():
            continue
        # If it's a header (#) or bold (**), make it a header tag
        if line.startswith("#") or line.startswith("**"):
            out += f"<h2>{line.strip('#*\n ')}</h2>"
        # If it's not a header, wrap it in a paragraph tag
        else:
            out += f"<p>{line.strip()}</p>"
    # Drop the bold tags
    out = _BOLD_PATTERN.sub("", out)
    return out