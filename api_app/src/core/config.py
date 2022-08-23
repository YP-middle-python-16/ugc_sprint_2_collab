import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field(env='PROJECT_NAME', default='statistics')

    # Корень проекта
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    KAFKA_FILM_VIEW_TOPIC: str = Field(env='KAFKA_FILM_VIEW_TOPIC', default='events_topic')
    KAFKA_FILM_LIKE_TOPIC: str = Field(env='KAFKA_FILM_LIKE_TOPIC', default='events_topic_like')
    KAFKA_FILM_COMMENT_TOPIC: str = Field(env='KAFKA_FILM_COMMENT_TOPIC', default='events_topic_comment')

    KAFKA_BROKERS: list = Field(env='KAFKA_BROKERS', default=['127.0.0.1:29092', '127.0.0.1:39092'])


settings = Settings()
