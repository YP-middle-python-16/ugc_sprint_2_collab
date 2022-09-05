import uuid
from random import randrange

USER_COUNT = 200
MOVIE_COUNT = 300
MOVIE_MAX_LEN = 180

USERS = [uuid.uuid4() for _ in range(1, USER_COUNT)]
MOVIES = [uuid.uuid4() for _ in range(1, MOVIE_COUNT)]

MOVIE_LENGTH = [randrange(MOVIE_MAX_LEN) for _ in range(1, MOVIE_COUNT)]

LIKE_MAX_LEN = 10
