from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_film_view_topic_name: str = Field(env="KAFKA_FILM_VIEW_TOPIC", default="events_topic")
    kafka_brokers: list = Field(env="KAFKA_BROKERS", default=["127.0.0.1:29092", "127.0.0.1:39092"])
    kafka_topics: list = Field(env="KAFKA_TOPICS", default=["events_topic"])
    kafka_group_id: str = Field(env="KAFKA_GROUP_ID", default="my-group")
    kafka_poll_timeout_ms: int = Field(env="KAFKA_POLL_TIMEOUT_MS", default=3000)
    clickhouse_host: str = Field(env="CLICKHOUSE_HOST", default="127.0.0.1")
    clickhouse_database: str = Field(env="CLICKHOUSE_DATABASE", default="events")
    clickhouse_film_view_table: str = Field(env="CLICKHOUSE_FILM_VIEW_TABLE", default="events")
    clickhouse_cluster: str = Field(env="CLICKHOUSE_CLUSTER", default="company_cluster")
    etl_batch_size: int = Field(env="BATCH_SIZE", default=500)
    etl_pause_duration: int = Field(env="PAUSE_DURATION", default=30)


settings = Settings()
