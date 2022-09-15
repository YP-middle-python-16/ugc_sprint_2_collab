from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    MESSAGES_BATCH_SIZE: int = Field(env="MESSAGES_BATCH_SIZE", default=10000)
    BATCHES: int = Field(env="BATCHES", default=10)

    API_TOPIC: str = Field(env="API_TOPIC", default="events_topic")

    API_HOST: str = Field(env="API_HOST", default="0.0.0.0")
    API_PORT: int = Field(env="API_PORT", default=8000)

    SLEEP_PAUSE: float = Field(env="SLEEP_PAUSE", default=0.5)


settings = Settings()
