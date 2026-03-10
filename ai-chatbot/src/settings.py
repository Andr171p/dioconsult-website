from typing import Literal

from datetime import datetime
from pathlib import Path

import pytz
from pydantic_settings import BaseSettings, SettingsConfigDict

TIMEZONE = pytz.timezone("Europe/Moscow")

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

SQLITE_URL = f"sqlite+aiosqlite:///{BASE_DIR / 'db.sqlite3'}"
CHECKPOINT_PATH = BASE_DIR / "checkpoint.sqlite"
CHROMA_PATH = BASE_DIR / ".chroma"
AGENT_CONFIG_FILE = BASE_DIR / "data" / "agent_config.json"

AVAILABLE_MODELS = Literal[
    "gemma-3-27b-it/latest",
    "aliceai-llm",
    "qwen3-235b-a22b-fp8/latest",
    "yandexgpt/rc"
]


def current_datetime() -> datetime:
    """Получение текущего времени в выбранном часовом поясе"""

    return datetime.now(TIMEZONE)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    yandex_cloud_folder_id: str = "<FOLDER_ID>"
    yandex_cloud_api_key: str = "<API_KEY>"
    yandex_cloud_base_url: str = "https://llm.api.cloud.yandex.net/v1"
    embeddings_base_url: str = "http://localhost:8000"

    def get_model_uri(self, model_name: str) -> str:
        return f"gpt://{self.yandex_cloud_folder_id}/{model_name}"


settings = Settings()
