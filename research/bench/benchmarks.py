import config
from hl_storage_kafka import KafkaStorage
from hl_storage_clickhouse import ClickhouseStorage
from hl_storage_null import DevNullStorage
from hl_storage_pg import PostgresStorage

BATCH_SEQUENCE = {
    'Kafka': {
        'storage': 'Kafka',
        'client': KafkaStorage(connect_param=config.KAFKA_CONNECT),
        'use': True,
        'use_insert': True,
        'use_select': False,
        'mode': 'single'
    },
    'Clickhouse single': {
        'storage': 'ClickHouse',
        'client': ClickhouseStorage(connect_param=config.CLICKHOUSE_CONNECT),
        'use': False,
        'use_insert': False,
        'use_select': False,
        'mode': 'single'
    },
    'Clickhouse batch': {
        'storage': 'ClickHouse',
        'client': ClickhouseStorage(connect_param=config.CLICKHOUSE_CONNECT),
        'use': True,
        'use_insert': True,
        'use_select': True,
        'mode': 'batch'
    },
    'Postgres batch': {
        'storage': 'Postgres',
        'client': PostgresStorage(connect_param=config.PG_DLS),
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
