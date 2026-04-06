import dataclasses

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
    title : str = dataclasses.field(init=False)
    description : str = ""
    link : str = dataclasses.field(init=False)

    def __post_init__(self):
        self.title = self.channel_name.lstrip("@")
        self.link = f"https://www.youtube.com/channel/{self.channel_id}"

@dataclasses.dataclass
class DB_Item:
    """
    The RSS Feed item model, with variables taken from the database

    Args:
        - video_name

    """
    video_name : str
    date_published : str
    url : str
    article : str
    title : str = dataclasses.field(init=False)
    link : str = dataclasses.field(init=False)
    description : str = dataclasses.field(init=False)
    pubDate : str = dataclasses.field(init=False)

    def __post_init__(self):
        self.title = self.video_name
        self.link = self.url
        self.description = self.article
        self.pubDate = self.date_published