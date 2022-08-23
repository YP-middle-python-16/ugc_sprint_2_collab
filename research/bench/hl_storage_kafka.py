import config
from kafka import KafkaProducer
from hl_storage_abstract import HiLoadStorage


class KafkaStorage(HiLoadStorage):
    def __init__(self, connect_param):
        self.producer = KafkaProducer(bootstrap_servers=connect_param)

    def insert(self, data=None):
        value = data.json()
        self.producer.send(
            topic=config.KAFKA_TOPIC,
            value=bytes(value, encoding="utf-8"),
            key=bytes(f'{data.user_id}_{data.movie_id}', encoding="utf-8")
        )

    def insert_batch(self, data=None, batch_size: int = 10):
        pass

    def select(self, data=None):
        pass