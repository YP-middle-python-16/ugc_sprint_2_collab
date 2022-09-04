from ugc.ugc_provider import UGCProvider
from ugc.ugc import ucg_config
import uuid
from random import randrange
from dataclasses import dataclass
from models.model import MovieViewEvent
from datetime import datetime


class UCGViewEvent(UGCProvider):
    def __init__(self):
        self.users = [uuid.uuid4() for i in range(1, ucg_config.USER_COUNT)]
        self.movies = [uuid.uuid4() for i in range(1, ucg_config.MOVIE_COUNT)]
        self.user_movie = [self.movies[randrange(ucg_config.MOVIE_COUNT - 1)]
                           for i in range(1, ucg_config.USER_COUNT)]

        self.movie_lengths = [randrange(ucg_config.MOVIE_MAX_LEN) for i in range(1, ucg_config.USER_COUNT)]

    def generate(self, limit):
        counter = 0
        while counter <= limit:
            counter = counter + 1

            time_now = datetime.now()
            time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")

            for user_counter in range(1, ucg_config.USER_COUNT - 1):
                user_current_movie_id = self.user_movie[user_counter]
                for tick in range(1, self.movie_lengths[user_counter]):
                    data = MovieViewEvent(
                        movie_id=str(user_current_movie_id),
                        user_id=str(self.users[user_counter]),
                        event_time=time_now,
                        view_run_time=tick
                    )
                    yield data

    def get_insert_query(self, data, sql_dialect):
        query = ''
        if sql_dialect == 'clickhouse':
            query = f"INSERT INTO movies_statistics.view_stat (movie_id, user_id, eventTime, view_run_time) " \
                    f"VALUES ('{data.movie_id}', '{data.user_id}', '{data.event_time}', {data.view_run_time})"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.movies_statistics (movie_id, user_id, event_time, view_run_time) ' \
                    'VALUES (%s, %s, %s, %s) '

        if sql_dialect == 'mongo':
            query = 'movies_statistics'

        return query

    def get_insert_query_batch(self, data, sql_dialect):
        query = ''
        if sql_dialect == 'clickhouse':
            rows = [f"('{row.movie_id}', '{row.user_id}', '{row.event_time}', {row.view_run_time})" for row in data]
            s = ","
            batch = s.join(rows)
            query = f"INSERT INTO movies_statistics.view_stat (movie_id, user_id, eventTime, view_run_time) " \
                    f"VALUES {batch}"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.movies_statistics (movie_id, user_id, event_time, view_run_time) ' \
                    'VALUES (%s, %s, %s, %s) '

        if sql_dialect == 'mongo':
            query = 'movies_statistics'

        return query

    def get_select_query(self, data, sql_dialect):
        query = ''

        if sql_dialect == 'clickhouse':
            query = f"SELECT  * FROM movies_statistics.view_stat " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'postgres':
            query = f"SELECT * FROM content.movies_statistics " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'mongo':
            query = 'movies_statistics'

        return query
