import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field(env='PROJECT_NAME', default='UGC')

    # Корень проекта
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # kafka settings
    KAFKA_FILM_VIEW_TOPIC: str = Field(env='KAFKA_FILM_VIEW_TOPIC', default='events_topic')
    KAFKA_FILM_LIKE_TOPIC: str = Field(env='KAFKA_FILM_LIKE_TOPIC', default='events_topic_like')
    KAFKA_FILM_COMMENT_TOPIC: str = Field(env='KAFKA_FILM_COMMENT_TOPIC', default='events_topic_comment')

    KAFKA_BROKERS: list = Field(env='KAFKA_BROKERS', default=['127.0.0.1:9092', '127.0.0.1:9092'])

    # mongo settings
    MONGO_CONNECTION = "mongodb://root:example@localhost:27017/"
    MONGO_DB = 'UGC'

    MONGO_TABLE_VIEW = 'views'
    MONGO_TABLE_LIKE = 'likes'
    MONGO_TABLE_COMMENT = 'comments'
    MONGO_TABLE_BOOKMARK = 'bookmark'

settings = Settings()
