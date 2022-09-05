from hl_storage_abstract import HiLoadStorage
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extras import DictCursor

import config


class PostgresStorage(HiLoadStorage):
    def __init__(self, connect_param=None):
        self.pg_conn = psycopg2.connect(**config.PG_DLS, cursor_factory=DictCursor)
        self.cur = self.pg_conn.cursor()

        self.insert_query = (
            "INSERT INTO content.movies_statistics (movie_id, user_id, event_time, view_run_time) " "VALUES (%s, %s, %s, %s) "
        )

    def insert(self, data=None):
        pass

    def insert_batch(self, data=None, batch_size: int = 10):
        cur = self.cur
        saved_table = []
        for row in data:
            r = row.dict()
            line = r.values()
            t = tuple(line)
            saved_table.append(t)
        # saved_table = [row.dict() for row in data]
        execute_batch(cur, self.insert_query, saved_table, page_size=len(data))
        self.pg_conn.commit()

    def select(self, data=None):
        select_query = f"SELECT * FROM content.movies_statistics " f"WHERE movie_id = '{data.movie_id}'"

        cur = self.cur
        cur.execute(select_query)

        pass
