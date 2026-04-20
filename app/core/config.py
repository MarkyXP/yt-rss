import datetime
import dataclasses
import os

from dotenv import load_dotenv

load_dotenv()

@dataclasses.dataclass
class Config:
    YTRSS_HOST = os.getenv("YTRSS_HOST", "0.0.0.0")
    YTRSS_PORT = int(os.getenv("YTRSS_PORT", 8000))
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemma4")
    TRANSCRIPTION_BASE_URL = os.getenv("TRANSCRIPTION_BASE_URL")
    DB_LOCATION = os.getenv("DB_LOCATION", "./database.db")
    UPDATE_INTERVAL_MINS = int(os.getenv("UPDATE_INTERVAL_MINS", 30))
    APP_VERSION = os.getenv("YTRSS_VERSION", f"DEBUG_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}")

CONFIG = Config()
