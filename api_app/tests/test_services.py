from unittest.mock import Mock

import kafka
import pytest
from fastapi.params import Depends

import db
from db.kafka import get_kafka_producer
from services.event_service import EventService
from services.service_locator import get_event_service

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


def test_get_event_service_use_depends_success():
    event_service = get_event_service()

    assert event_service is not None
    assert isinstance(event_service, EventService)
    assert event_service.kafka_producer is not None
    assert isinstance(event_service.kafka_producer, Depends)


def test_get_event_service_send_param_success():
    event_service = get_event_service(kafka_producer=Mock())

    assert event_service is not None
    assert isinstance(event_service, EventService)
    assert isinstance(event_service.kafka_producer, Mock)
    assert not event_service.kafka_producer.called


async def test_get_kafka_producer_empty_success():
    kafka_producer = await get_kafka_producer()

    assert kafka_producer is None


async def test_get_kafka_producer_mocked_success():
    db.kafka.kafka_producer = Mock()
    kafka_producer = await get_kafka_producer()

    assert kafka_producer is not None
    assert isinstance(kafka_producer, Mock)
