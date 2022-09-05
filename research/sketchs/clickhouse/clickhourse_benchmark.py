import uuid
from random import randrange
from datetime import datetime

from clickhouse_driver import Client

MESSAGES_BATCH_SIZE = 1000000
BATCHES = 100

TOPIC = "views"
USER_COUNT = 2000
MOVIE_COUNT = 30
MOVIE_MAX_LEN = 180

users = [uuid.uuid4() for i in range(1, USER_COUNT)]
movies = [uuid.uuid4() for i in range(1, MOVIE_COUNT)]
movie_lengths = [randrange(MOVIE_MAX_LEN) for i in range(1, MOVIE_COUNT)]

client = Client(host="localhost")

time_now = datetime.now()
time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")

for i in range(1, BATCHES):
    for user_id in users:
        user_current_movie_id = movies[randrange(MOVIE_COUNT - 1)]
        for tick in movie_lengths:
            query = (
                f"INSERT INTO movies_statistics.view_stat (movie_id, user_id, eventTime, view_run_time) "
                f"VALUES ('{user_current_movie_id}', '{user_id}', '{time_now}', {tick})"
            )
            client.execute(query)

    print(i)
