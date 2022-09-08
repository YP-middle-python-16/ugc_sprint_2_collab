from functools import lru_cache

from db.async_message_queue import AsyncMessageQueue
from db.kafka import get_kafka_producer
from db.async_storage import AsyncStorage
from db.mongo import get_mongo_client
from fastapi import Depends
from services.event_service import EventService
from services.doc_service import DocService


@lru_cache()
def get_event_service(
        kafka_producer: AsyncMessageQueue = Depends(get_kafka_producer)
) -> EventService:
    return EventService(kafka_producer=kafka_producer)

def get_storage_service(
        mongo_client: AsyncStorage = Depends(get_mongo_client)
) -> DocService:
    return DocService(mongo_client = mongo_client)
