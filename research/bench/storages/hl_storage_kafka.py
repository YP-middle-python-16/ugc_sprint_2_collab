from core import config
from kafka import KafkaProducer
from storages.hl_storage import HiLoadStorage


class KafkaStorage(HiLoadStorage):
    def __init__(self, connect_param):
        self.producer = KafkaProducer(bootstrap_servers=connect_param)
        self.sql_dialect = None
        self.label = 'Kafka'

    def insert(self, data=None, query: str = None):
        value = data.json()
        self.producer.send(
            topic=config.KAFKA_TOPIC,
            value=bytes(value, encoding="utf-8"),
            key=bytes(f'{data.user_id}_{data.movie_id}', encoding="utf-8")
        )

    def insert_batch(self, data=None,  query: str = None):
        pass

    def select(self, data=None, query: str = None):
        pass