from core.config import settings
from storages.hl_storage_kafka import KafkaStorage
from storages.hl_storage_clickhouse import ClickhouseStorage
from storages.hl_storage_null import DevNullStorage
from storages.hl_storage_pg import PostgresStorage
from storages.hl_storage_mongo import MongoDBStorage

STORAGES_CATALOG = {
    'Kafka': {
        'storage': 'Kafka',
        'client': DevNullStorage(),  # KafkaStorage(connect_param=settings.KAFKA_CONNECT),
        'use': False,
        'use_insert': True,
        'use_select': False,
        'mode': 'single'
    },
    'Clickhouse single': {
        'storage': 'ClickHouse',
        'client': ClickhouseStorage(connect_param=settings.CLICKHOUSE_CONNECT),
        'use': False,
        'use_insert': False,
        'use_select': False,
        'mode': 'single'
    },
    'Clickhouse batch': {
        'storage': 'ClickHouse',
        'client': ClickhouseStorage(connect_param=settings.CLICKHOUSE_CONNECT),
        'use': True,
        'use_insert': True,
        'use_select': True,
        'mode': 'batch'
    },
    'Mongo_batch': {
        'storage': 'MondoDB',
        'client': MongoDBStorage(connect_param=settings.MONGODB_CONNECT),
        'use': True,
        'use_insert': True,
        'use_select': True,
        'mode': 'batch'
    },
    'Postgres batch': {
        'storage': 'Postgres',
        'client': PostgresStorage(connect_param=settings.PG_DLS),
        'use': True,
        'use_insert': True,
        'use_select': True,
        'mode': 'batch'
    },
    'DevNull': {
        'storage': 'Dev/Null/',
        'client': DevNullStorage(),
        'use': True,
        'use_insert': True,
        'use_select': True,
        'mode': 'single'
    }
}
