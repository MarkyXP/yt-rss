from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
    TRANSCRIPTION_BASE_URL = os.getenv("TRANSCRIPTION_BASE_URL")
    DB_LOCATION = os.getenv("DB_LOCATION", "./database.db")
    UPDATE_INTERVAL_MINS = int(os.getenv("UPDATE_INTERVAL_MINS", 30))

CONFIG = Config()
