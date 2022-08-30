import logging

import aiokafka
import logstash
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.v1 import events
from core.config import settings
from core.logger import LOGGING
from db import kafka
from utils import backoff, RequestIdFilter

sentry_sdk.init(dsn=settings.SENTRY_DSN,
                integrations=[
                    StarletteIntegration(),
                    FastApiIntegration(),
                ],
                traces_sample_rate=1.0,
                )

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
    if settings.CHECK_HEADERS and not request_id:
        raise RuntimeError('request id is required')
    return await call_next(request)


# Подключаем роутер к серверу, указав префикс /v1/events
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix='/api/v1/event', tags=['Event'])
# Добавим middleware для Sentry
app.add_middleware(SentryAsgiMiddleware)
# Добавим фильтр логов по хедеру X-Request-Id
uvicorn.config.logger.addFilter(RequestIdFilter())
uvicorn.config.logger.addHandler(logstash.LogstashHandler(settings.LOGSTASH_HOST, settings.LOGSTASH_PORT, version=1))

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        log_config=LOGGING,
        log_level=logging.DEBUG,
        port=8000,
    )
