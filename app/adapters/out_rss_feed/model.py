import dataclasses
import html
import re

_BOLD_PATTERN = re.compile(r"(\*\*)+")

@dataclasses.dataclass
class DB_Channel:
    """
    The RSS Feed high level model, with variables taken from the database

    Args:
        - channel_id: The YouTube channel ID
        - channel_name: The YouTube channel name

    Returns:
        - title: The channel's title (YouTube channel name without the @ symbol)
        - description: The channel's description (blank)
        - link: The channel's YouTube URL (https://www.youtube.com/channel/<channel_id>)
    """
    channel_id : str
    channel_name : str
    channel_description : str
    title : str = dataclasses.field(init=False)
    link : str = dataclasses.field(init=False)
    description : str = dataclasses.field(init=False)


    def __post_init__(self):
        self.title = html.escape(self.channel_name.lstrip("@"))
        self.link = html.escape(f"https://www.youtube.com/channel/{self.channel_id}")
        self.description = html.escape(self.channel_description)
        pass

@dataclasses.dataclass
class DB_Item:
    """
    The RSS Feed item model, with variables taken from the database

    Args:
        - video_name (str) : Name of the video from YouTube (e.g. 'EEVblog 1742 - Today in the Dumpster Room')
        - date_published (str) : Date the video was published on YouTube (e.g. '2026-03-31T10:00:17+00:00')
        - url (str) : URL of the video (e.g. 'https://www.youtube.com/watch?v=HLmty8KcOd4')
        - thumbnail (str) : URL for the youtube thumbnail (e.g. 'https://i1.ytimg.com/vi/HLmty8KcOd4/hqdefault.jpg')
        - article (str) : Raw LLM generated article (e.g. '# Main Topics\n...')
    
    Returns:
        - title (str) : RSS Item title (e.g. 'EEVblog 1742 - Today in the Dumpster Room')

    """
    video_name : str
    date_published : str
    url : str       # URL of the video
    thumbnail : str # URL for the youtube thumbnail
    article : str   # Raw LLM generated article
    title : str = dataclasses.field(init=False)
    link : str = dataclasses.field(init=False)
    description : str = dataclasses.field(init=False) # Used for RSS Item description & content
    pubDate : str = dataclasses.field(init=False)

    def __post_init__(self):
        self.title = html.escape(self.video_name)
        self.link = html.escape(self.url)
        reformatted_article = self._generate_rss_item_description()
        self.description = reformatted_article
        self.pubDate = html.escape(self.date_published)

    def _generate_rss_item_description(self):
        """
        Combines the thumbnail & article into a single string for RSS description.
        """
        out = f'<img src="{self.thumbnail}">'
        for line in self.article.split("\n"):
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

    
    @staticmethod
    def from_scrapers(self):
        return self