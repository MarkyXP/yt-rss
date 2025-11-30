"""

References:
> https://github.com/fastapi/sqlmodel/issues/150
"""

import functools
import typing

from pydantic import computed_field
from sqlmodel import Field, SQLModel

from natural_text import generate_article


class YT_Channel(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    channel_handle: str = Field(unique=True)
