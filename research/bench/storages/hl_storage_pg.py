import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extras import DictCursor

from core import config
from storages.hl_storage import HiLoadStorage


class PostgresStorage(HiLoadStorage):
    def __init__(self, connect_param=None):
        self.sql_dialect = 'clickhouse'
        self.pg_conn = psycopg2.connect(**config.PG_DLS, cursor_factory=DictCursor)
        self.cur = self.pg_conn.cursor()

        self.insert_query = 'INSERT INTO content.movies_statistics (movie_id, user_id, event_time, view_run_time) ' \
                            'VALUES (%s, %s, %s, %s) '



    def insert_old(self, data=None):
        pass

    def insert_batch_old(self, data=None, batch_size: int = 10):
        cur = self.cur
        saved_table = []
        for row in data:
            r = row.dict()
            l = r.values()
            t = tuple(l)
            saved_table.append(t)
        # saved_table = [row.dict() for row in data]
        execute_batch(cur, self.insert_query, saved_table, page_size=len(data))
        self.pg_conn.commit()

    def select_old(self, data=None):
        select_query = f"SELECT * FROM content.movies_statistics " \
                       f"WHERE movie_id = '{data.movie_id}'"

        cur = self.cur
        cur.execute(select_query)

        pass

