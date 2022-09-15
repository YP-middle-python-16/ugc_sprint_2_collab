from clickhouse_driver import Client
from storages.hl_storage import HiLoadStorage


class ClickhouseStorage(HiLoadStorage):
    def __init__(self, connect_param):
        self.client = Client(host=connect_param)
        self.sql_dialect = 'clickhouse'
        self.label = 'ClickHouse'

    def insert(self, data=None, query: str = None):
        self.client.execute(query)

    def insert_batch(self, data=None, query: str = None):
        self.client.execute(query)

    def select(self, data=None, query: str = None):
        self.client.execute(query)
