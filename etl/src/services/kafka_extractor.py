import json
import typing as t

from kafka import (
    KafkaConsumer as _KafkaConsumer,
    OffsetAndMetadata,
    TopicPartition,
)
from kafka.consumer.fetcher import ConsumerRecord

from core.config import settings
from models import Message, FilmViewEvent
from services import logger


class KafkaExtractor:
    def __init__(
        self,
        bootstrap_servers: str,
        topic_list: list,
        group_id: str = None,
        batch_size: int = 500,
        auto_offset_reset: str = "earliest",
        **kwargs,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._topic_list = topic_list
        self._group_id = group_id
        self._meta: dict[str, t.Any] = kwargs
        self._config: dict[str, t.Any] = {}
        self._consumer: t.Optional[_KafkaConsumer] = None
        self._max_poll_records = batch_size
        self._auto_offset_reset = auto_offset_reset

    @property
    def config(self):
        if not self._config:
            self._config.update(
                {
                    "bootstrap_servers": self._bootstrap_servers,
                    "group_id": self._group_id,
                    "max_poll_records": self._max_poll_records,
                    "auto_offset_reset": self._auto_offset_reset,
                    **self._meta,
                },
            )
        return self._config

    @property
    def consumer(self) -> _KafkaConsumer:
        if self._consumer:
            return self._consumer

        consumer: _KafkaConsumer = _KafkaConsumer(value_deserializer=lambda x: json.loads(x.decode("utf-8")), **self.config)
        logger.info(f"Kafka consumer is started with options: {self.config}")

        self._consumer = consumer
        return self._consumer

    def list_messages(self, timeout_ms: int = settings.kafka_poll_timeout_ms) -> t.Generator:
        """
        Метод вычитывает сообщения из топика.
        :param timeout_ms: Таймаут ожидания новых сообщений в Kafka при выполнении запроса poll.
        """
        logger.info(f'Start listing messages from topic "{self._topic_list}"')
        messages_dict = self.consumer.poll(timeout_ms)
        if not messages_dict:
            logger.info(f'There are no new messages in Kafka topic "{self._topic_list}"')
            return
        for consumer_record_list in messages_dict.values():
            for consumer_record in consumer_record_list:
                logger.info(
                    f'Got message from offset="{consumer_record.offset}" ' f'and partition="{consumer_record.partition}"'
                )
                yield Message(topic=consumer_record.topic, body=FilmViewEvent(**consumer_record.value))
                self.commit(consumer_record)

    def subscribe(self):
        """
        Подписка на топик
        """
        logger.info(f"Describe to topic {self._topic_list}")
        self.consumer.subscribe(self._topic_list)

    def commit(self, message: ConsumerRecord):
        """
        Метод для коммита сообщения
        :param message: сообщение типа ConsumerRecord
        """
        if not self._group_id:
            return
        logger.info(f"Commit message from offset={message.offset}")
        tp = TopicPartition(message.topic, message.partition)
        meta = self.consumer.partitions_for_topic(message.topic)
        options = {tp: OffsetAndMetadata(message.offset + 1, meta)}
        self.consumer.commit(options)

    def close(self):
        """
        Метод закрывает соединение консьюмера с kafka
        """
        logger.info("Close Kafka consumer")
        self.consumer.close()
        self._consumer = None
