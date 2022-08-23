import aiokafka
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.logger import logger

from api.v1 import events
from core.config import settings
from db import kafka
from utils import backoff

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
@backoff(border_sleep_time=20)
async def startup():
    kafka.kafka_producer = aiokafka.AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKERS)
    await kafka.kafka_producer.start()
    logger.info('kafka is ok')


@app.on_event('shutdown')
async def shutdown():
    await kafka.kafka_producer.stop()


# Подключаем роутер к серверу, указав префикс /v1/events
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix='/api/v1/event', tags=['Event'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
