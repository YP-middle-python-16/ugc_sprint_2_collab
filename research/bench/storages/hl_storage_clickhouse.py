from clickhouse_driver import Client
from storages.hl_storage import HiLoadStorage


class ClickhouseStorage(HiLoadStorage):
    def __init__(self, connect_param):
        self.client = Client(host=connect_param)
        self.sql_dialect = 'clickhouse'

    def insert(self, data=None):
        query = f"INSERT INTO movies_statistics.view_stat (movie_id, user_id, eventTime, view_run_time) " \
                f"VALUES ('{data.movie_id}', '{data.user_id}', '{data.event_time}', {data.view_run_time})"
        self.client.execute(query)

    def insert_batch(self, data=None, batch_size: int = 10):
        rows = [f"('{row.movie_id}', '{row.user_id}', '{row.event_time}', {row.view_run_time})" for row in data]
        s = ","
        batch = s.join(rows)
        query = f"INSERT INTO movies_statistics.view_stat (movie_id, user_id, eventTime, view_run_time) " \
                f"VALUES {batch}"
        self.client.execute(query)

    def select(self, data=None):
        query = f"SELECT  * FROM movies_statistics.view_stat " \
                f"WHERE movie_id = '{data.movie_id}'"
        self.client.execute(query)
