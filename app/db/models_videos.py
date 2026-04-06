from dataclasses import dataclass

@dataclass
class DB_Video:
    id : str
    channel_name
    video_name
    date_published
    url
    thumbnail
    transcript
    article
    created_at
    updated_at