import uuid
from random import randrange

from kafka import KafkaProducer
from time import sleep

MESSAGES_BATCH_SIZE = 1000000
BATCHES = 100

TOPIC = "views"
USER_COUNT = 2000
MOVIE_COUNT = 30
MOVIE_MAX_LEN = 180

users = [uuid.uuid4() for i in range(1, USER_COUNT)]
movies = [uuid.uuid4() for i in range(1, MOVIE_COUNT)]
movie_lengths = [randrange(MOVIE_MAX_LEN) for i in range(1, MOVIE_COUNT)]

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for i in range(1, BATCHES):
    for user_id in users:
        user_current_movie_id = movies[randrange(MOVIE_COUNT-1)]
        for tick in movie_lengths:
            producer.send(
                topic=TOPIC,
                value=bytes(str(tick), encoding="utf-8"),
                key=bytes(f'{user_id}_{user_current_movie_id}', encoding="utf-8")
            )
    print(i)
