from pydantic import BaseSettings, Field


class PGSettings(BaseSettings):
    dbname: str = Field(env='DB_NAME', default='movies_database')
    user: str = Field(env='DB_USER', default='app')
    password: str = Field(env='DB_PASSWORD', default='123qwe')
    host: str = Field(env='DB_HOST', default='0.0.0.0')
    port: int = Field(env='DB_PORT', default=5432)


class Settings(BaseSettings):
    MESSAGES_BATCH_SIZE: int = Field(env='MESSAGES_BATCH_SIZE', default=1000000)
    BATCHES: int = Field(env='BATCHES', default=10)

    USER_COUNT: int = Field(env='USER_COUNT', default=200)
    MOVIE_COUNT: int = Field(env='MOVIE_COUNT', default=400)
    MOVIE_MAX_LEN: int = Field(env='MOVIE_MAX_LEN', default=180)

    KAFKA_TOPIC: str = Field(env='KAFKA_TOPIC', default='views')
    KAFKA_CONNECT: list = Field(env='KAFKA_CONNECT', default=['localhost:9092'])

    CLICKHOUSE_CONNECT: str = Field(env='CLICKHOUSE_CONNECT', default='localhost')

    MONGODB_CONNECT: str = Field(env='MONGODB_CONNECT', default='mongodb://root:example@localhost/')

    PG_DLS: dict = PGSettings().dict()


settings = Settings()
