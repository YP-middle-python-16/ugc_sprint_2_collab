from collections import defaultdict
from typing import Generator

from config import settings


class DataTransformer:
    @classmethod
    def get_table_name_by_topic_name(cls, topic_name: str) -> str:
        return {
            settings.kafka_film_view_topic_name: settings.clickhouse_film_view_table,
        }[topic_name]

    @classmethod
    def get_aggregate_topic_data(cls, data: Generator) -> dict:
        res = defaultdict(list)
        for model in data:
            res[cls.get_table_name_by_topic_name(model.topic)].append(model.body.dict())

        return res
