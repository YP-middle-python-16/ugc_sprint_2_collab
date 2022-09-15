import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extras import DictCursor

from core import config
from storages.hl_storage import HiLoadStorage


class PostgresStorage(HiLoadStorage):
    def __init__(self, connect_param=None):
        self.sql_dialect = 'postgres'
        self.label = 'Postgres'

        self.pg_conn = psycopg2.connect(**config.PG_DLS, cursor_factory=DictCursor)
        self.cur = self.pg_conn.cursor()

    def insert(self, data=None, query: str = None):
        pass

    def insert_batch(self, data=None, queue: str = None):
        cur = self.cur
        saved_table = []
        for row in data:
            r = row.dict()
            li = r.values()
            t = tuple(li)
            saved_table.append(t)

        execute_batch(cur, queue, saved_table, page_size=len(data))

    def select(self, data=None, queue: str = None):
        cur = self.cur
        cur.execute(queue)
