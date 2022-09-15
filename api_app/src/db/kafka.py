from typing import Optional

from aiokafka.producer import AIOKafkaProducer

kafka_producer: Optional[AIOKafkaProducer] = None


# Функция понадобится при внедрении зависимостей
async def get_kafka_producer() -> AIOKafkaProducer:
    return kafka_producer
