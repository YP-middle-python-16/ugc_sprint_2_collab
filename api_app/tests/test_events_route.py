from unittest.mock import MagicMock, patch, AsyncMock

import pytest

# All test coroutines will be treated as marked.
from main import startup

pytestmark = pytest.mark.asyncio


@patch('services.event_service.EventService.send_message')
def test_send_event_message_success(send_message_mock: MagicMock, client):
    response = client.post('/api/v1/event/',
                           headers={'Content-Type': 'application/json'},
                           json={
                               'key': 'test_key',
                               'value': 'test_value'
                           })
    assert response.status_code == 200
    assert response.json() == {'head': 'ok', 'body': 'all ok'}
    assert send_message_mock.called


@patch('services.event_service.EventService.send_message')
def test_send_event_message_empty_msg_fail(send_message_mock: MagicMock, client):
    response = client.post('/api/v1/event/',
                           headers={'Content-Type': 'application/json'})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body'],
                                           'msg': 'field required',
                                           'type': 'value_error.missing'}]}
    assert not send_message_mock.called


def test_send_event_message_none_kafka_fail(client):
    with pytest.raises(AttributeError) as e:
        client.post('/api/v1/event/',
                    headers={'Content-Type': 'application/json'},
                    json={
                        'key': 'test_key',
                        'value': 'test_value'
                    })
    assert e.value.args[0] == "'NoneType' object has no attribute 'send'"


@patch('aiokafka.AIOKafkaProducer.start')
async def test_send_event_message_error_on_kafka_fail(kafka_start_mock: AsyncMock, client):
    await startup()
    with pytest.raises(RuntimeError) as e:
        client.post('/api/v1/event/',
                    headers={'Content-Type': 'application/json'},
                    json={
                        'key': 'test_key',
                        'value': 'test_value'
                    })
    assert 'attached to a different loop' in e.value.args[0]
    assert kafka_start_mock.called
