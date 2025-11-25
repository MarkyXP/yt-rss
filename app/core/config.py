import json
import os
from dataclasses import dataclass
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Prompts(Enum):
    GENERATE_ARTICLE = "generate_article"

    def get_sys_prompt(self):
        with open(f"app/prompts/{self.value}.txt", "r") as f:
            return f.read()


@dataclass
class Config:
    PROMPTS = Prompts
    GROQ_API_KEY: str
    GROQ_MODEL: str


with open("app/core/config.json", "r") as f:
    CONFIG = Config(**json.load(f), GROQ_API_KEY=os.getenv("GROQ_API_KEY"))
