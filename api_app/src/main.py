import logging
import uuid

import aiokafka
import logstash
import sentry_sdk
import uvicorn
from fastapi.logger import logger
from pymongo import MongoClient
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.v1 import events, likes, comments, bookmarks
from core.config import settings
from core.logger import configure_logging, logger, LOGGING
from db import kafka
from db import mongo
from utils import backoff

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
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
    on_startup=[configure_logging],
)


@app.on_event('startup')
@backoff(border_sleep_time=20)
async def startup():
    kafka.kafka_producer = aiokafka.AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKERS)
    await kafka.kafka_producer.start()
    logger.info('kafka is ok')

    mongo.mongo_client = MongoClient(settings.MONGO_CONNECTION)


@app.on_event('shutdown')
async def shutdown():
    logger.info("kafka will be stopped")
    await kafka.kafka_producer.stop()


@app.middleware('http')
async def logging(request: Request, call_next):
    # check header
    request_id = request.headers.get("X-Request-Id")
    if settings.CHECK_HEADERS and not request_id:
        raise RuntimeError("request id is required")
    response = await call_next(request)
    # add tag for logs
    custom_logger = logging.LoggerAdapter(
        logger, extra={'tag': 'ugc_api', 'request_id': request_id}
    )
    custom_logger.info(request)
    return response


# Подключаем роутер к серверу, указав префикс /v1/****
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix="/api/v1/event", tags=["Event"])
# Добавим middleware для работы с X-Request-Id (https://github.com/snok/asgi-correlation-id)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
    generator=lambda: uuid.uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)
# Добавим middleware для Sentry
app = SentryAsgiMiddleware(app)  # type: ignore
logger.addHandler(logstash.LogstashHandler(settings.LOGSTASH_HOST, settings.LOGSTASH_PORT, version=1))
app.include_router(events.router, prefix='/api/v1/event', tags=['Event'])
app.include_router(comments.router, prefix='/api/v1/comments', tags=['Comment'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['Likes'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['Bookmarks'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
