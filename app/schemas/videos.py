"""

References:
> https://github.com/fastapi/sqlmodel/issues/150
"""

import functools
import typing

from pydantic import computed_field
from sqlmodel import Field, SQLModel

from natural_text import generate_article


class Videos(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    url: str
    channel: str = Field(index=True)
    date: float = Field(index=True)
    duration: str
    duration_seconds: int
    thumbnail: str
    transcript: str
    body: typing.Optional[str]

    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    if not self.body:
    #        self.body = generate_article()
    @property
    def body(self):
        return generate_article(self.transcript)
