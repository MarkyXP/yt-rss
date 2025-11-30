import json
from dataclasses import dataclass
from enum import Enum


class Prompts(Enum):
    GENERATE_ARTICLE = "generate_article"

    def get_sys_prompt(self):
        with open(f"app/prompts/{self.value}.txt", "r") as f:
            return f.read()


@dataclass
class Config:
    PROMPTS = Prompts
    app_name : str
    app_icon : str
    db_location : str


with open("app/core/config.json", "r") as f:
    CONFIG = Config(**json.load(f))
