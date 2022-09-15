import json

from ugc.ugc_provider import UGCProvider
from models.model import LikeEvent


class UGCLike(UGCProvider):
    def __init__(self):
        self.label = 'Like'

    def generate(self, limit):
        counter = 0
        while counter <= limit:
            counter = counter + 1
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
            rows = [f"('{row.movie_id}', '{row.user_id}')" for row in data]
            s = ","
            batch = s.join(rows)
            query = f"INSERT INTO movies_statistics.likes (movie_id, user_id) " \
                    f"VALUES {batch}"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.likes (movie_id, user_id) ' \
                    'VALUES (%s, %s) '

        if sql_dialect == 'mongo':
            query = 'likes'

        return query

    def get_select_query(self, data, sql_dialect='postgres'):
        query = ''

        if sql_dialect == 'clickhouse':
            query = f"SELECT  * FROM movies_statistics.likes " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'postgres':
            query = f"SELECT * FROM content.likes " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'mongo':
            collection = 'likes'
            data_select = {'movie_id': data.movie_id}

            json_object = json.dumps(data_select, indent=4)
            query = (collection, json_object)

        return query
