import aiokafka
import uvicorn
from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse

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


@app.middleware('http')
async def before_request(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')
    return await call_next(request)


# Подключаем роутер к серверу, указав префикс /v1/events
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix='/api/v1/event', tags=['Event'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
