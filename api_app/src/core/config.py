import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="statistics")

    # Корень проекта
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    KAFKA_FILM_VIEW_TOPIC: str = Field(env="KAFKA_FILM_VIEW_TOPIC", default="events_topic")
    KAFKA_BROKERS: list = Field(env="KAFKA_BROKERS", default=["127.0.0.1:29092", "127.0.0.1:39092"])

    CHECK_HEADERS: bool = Field(env="CHECK_HEADERS", default=False)

    SENTRY_DSN: str = Field(
        env="SENTRY_DSN", default="https://2d58bf3f78894d5aa32824671303a1ef@o1377615.ingest.sentry.io/6691544"
    )

    LOGSTASH_HOST: str = Field(env="LOGSTASH_HOST", default="logstash")
    LOGSTASH_PORT: str = Field(env="LOGSTASH_PORT", default=5044)


settings = Settings()
