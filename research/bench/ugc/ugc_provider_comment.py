import json

from ugc.ugc_provider import UGCProvider
from models.model import Comment


class UGCComment(UGCProvider):
    def __init__(self):
        self.label = 'Comment'

    def generate(self, limit):
        counter = 0
        while counter <= limit:
            counter = counter + 1
            yield Comment.random()


    def get_insert_query(self, data, sql_dialect='postgres'):
        query = ''
        if sql_dialect == 'clickhouse':
            query = f"INSERT INTO movies_statistics.comments (movie_id, user_id, event_time, title, body, score) " \
                    f"VALUES ('{data.movie_id}', '{data.user_id}', '{data.event_time}','{data.title}'," \
                    f" '{data.body}', '{data.score}')"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.movies_comments (movie_id, user_id, event_time, title, body, score) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s ) '

        if sql_dialect == 'mongo':
            query = 'likes'

        return query

    def get_insert_query_batch(self, data, sql_dialect='postgres'):
        query = ''
        if sql_dialect == 'clickhouse':
            rows = [f"('{row.movie_id}', '{row.user_id}', '{row.event_time}', '{row.title}', '{row.body}', '{row.score}')" for row in data]
            s = ","
            batch = s.join(rows)
            query = f"INSERT INTO movies_statistics.comments (movie_id, user_id, event_time, title, body, score) " \
                    f"VALUES {batch}"

        if sql_dialect == 'postgres':
            query = 'INSERT INTO content.comments (movie_id, user_id, event_time, title, body, score) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s ) '

        if sql_dialect == 'mongo':
            query = 'comments'

        return query

    def get_select_query(self, data, sql_dialect='postgres'):
        query = ''

        if sql_dialect == 'clickhouse':
            query = f"SELECT  * FROM movies_statistics.comments " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'postgres':
            query = f"SELECT * FROM content.comments " \
                    f"WHERE movie_id = '{data.movie_id}'"

        if sql_dialect == 'mongo':
            collection = 'comments'
            data_select = {'movie_id': data.movie_id}

            json_object = json.dumps(data_select, indent=4)
            query = (collection, json_object)

        return query
