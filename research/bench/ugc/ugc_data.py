import uuid
from random import randrange
from dataclasses import dataclass
from models.model import MovieViewEvent
from datetime import datetime
from ugc.ugc import ucg_config


@dataclass
class ugc_provider:
    def __init__(self):
        self.users = []
        self.movies = []
        self.user_movie = []
        self.movie_lengths = []

    def generate_dataset(self):
        self.users = [uuid.uuid4() for i in range(1, ucg_config.USER_COUNT)]
        self.movies = [uuid.uuid4() for i in range(1, ucg_config.MOVIE_COUNT)]
        self.user_movie = [self.movies[randrange(ucg_config.MOVIE_COUNT - 1)]
                           for i in range(1, ucg_config.USER_COUNT)]

        self.movie_lengths = [randrange(ucg_config.MOVIE_MAX_LEN) for i in range(1, ucg_config.USER_COUNT)]

    def generate_view_event(self):
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

    def generate_like(self, count):
        pass

    def generate_comment(self):
        pass

    def generate_bookmark(self):
        pass
