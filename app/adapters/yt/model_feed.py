from dataclasses import dataclass

@dataclass
class Channel_ID:
    """The ID details for a channel"""
    id : str
    name : str

class Entry:
    id : str
    title : str
    author : Author
    published : str
    updated : str
    href : str
    thumbnail : str
    description : str

    def __init__(self, details):
        """Youtube Video details

        Args:
            - id (str) : The video ID (e.g. 'dQw4w9WgXcQ')
            - title (str) : The video title (e.g. 'Eevblog #40: 2023-05-0
            - author (Author): The video author
            - published (str): The video published date (e.g. '2023-05-04T18:00:
            - updated (str): The video updated date (e.g. '2023-05-04T18:00:
            - href (str): The video URL (e.g. 'https://www.youtube.com/watch?v=dQw4w9WgXcQ
            - thumbnail (str): The video thumbnail URL (e.g. 'https://i.ytimg.com/vi/dQw4w9WgX
        """
        self.id = details['yt:videoId']
        self.title = details['title']
        self.author = Author(**details['author'])
        self.published = details['published']
        self.updated = details['updated']
        self.href = details['link']['@href']
        self.thumbnail = details['media:group']['media:thumbnail']['@url']
        self.description = details['media:group']['media:description']


@dataclass
class Author:
    """Youtube Author Details
    
    Args:
        - name (str) : The author's name (e.g. 'EEVblog')
        - uri (str) : The author's URI (e.g. 'https://www.youtube.com/channel/UC2DjFE7Xf11URZqWBigcVOQ')
    """
    name: str
    uri: str

class Feed:
    id: str
    title: str
    published : str
    author : Author
    entries : list[Entry]
    def __init__(self, details):
        """
        Youtube Feed

        Args:
            - id (str) : The channels ID (e.g. '2DjFE7Xf11URZqWBigcVOQ')
            - title (str) : The channel's title (e.g. 'EEVblog')
            - published (str) : In ISO 8601 format (e.g. '2009-04-04T22:27:18+00:00')
            - author (Author) : The channel's author
            - entries (list[Entry]) : The channel's videos
        """
        self.id = details["yt:channelId"]
        self.title = details["title"]
        self.published = details["published"] # '2009-04-04T22:27:18+00:00'
        self.author = Author(**details["author"])
        self.entries = [Entry(e) for e in details.get("entry", [])]
