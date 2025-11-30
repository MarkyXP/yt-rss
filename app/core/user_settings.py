import json
import os
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    LLM_ENDPOINT : str
    LLM_API_KEY : str
    LLM_MODEL : str


SETTINGS = Settings(
    LLM_ENDPOINT=os.getenv("LLM_ENDPOINT"),
    LLM_API_KEY = os.getenv("LLM_API_KEY"),
    LLM_MODEL = os.getenv("LLM_MODEL")
)


