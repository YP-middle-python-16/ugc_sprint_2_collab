from ugc.ugc_provider import UGCProvider
from models.model import LikeEvent


class UGCLike(UGCProvider):
    def __init__(self):
        pass

    def generate(self, limit):
        counter = 0
        while counter <= limit:
            counter = counter+1
            yield LikeEvent.random()

    def get_insert_query(self, data, sql_dialect='postgres'):
        query = ''
        if sql_dialect == 'clickhouse':
            query = f"INSERT INTO movies_statistics.likes (movie_id, user_id) " \
                    f"VALUES ('{data.movie_id}', '{data.user_id}')"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.movies_likes (movie_id, user_id) ' \
                    'VALUES (%s, %s) '

        if sql_dialect == 'mongo':
            query = 'likes'

        return query

    def get_insert_query_batch(self, data, sql_dialect='postgres'):
        query = ''
        if sql_dialect == 'clickhouse':
            query = f"INSERT INTO movies_statistics.likes (movie_id, user_id) " \
                    f"VALUES ('{data.movie_id}', '{data.user_id}', '{data.event_time}', {data.view_run_time})"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.movies_statistics (movie_id, user_id, event_time, view_run_time) ' \
                    'VALUES (%s, %s, %s, %s) '

        return query

    def get_select_query(self, data, sql_dialect='postgres'):
        query = ''

        if sql_dialect == 'clickhouse':
            query = f"SELECT  * FROM movies_statistics.view_stat " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'postgres':
            query = f"SELECT * FROM content.movies_statistics " \
                    f"WHERE movie_id = '{data.movie_id}'"

        return query

