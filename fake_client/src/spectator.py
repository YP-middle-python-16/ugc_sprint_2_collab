from datetime import datetime
from random import randrange
from typing import Optional

import fake_data
from models import FilmViewEvent


class Spectator:
    def __init__(self, user_id, movie_id, length):
        self.length = length
        self.movie_id = movie_id
        self.user_id = user_id

        self.key = None

        self.current_second = None
        self.end_second = None
        self.start_second = None

        self.start_watch_movie(movie_id, length)

    def start_watch_movie(self, movie_id, length):
        self.movie_id = movie_id
        self.length = length

        rnd1 = randrange(fake_data.MOVIE_MAX_LEN)
        rnd2 = randrange(fake_data.MOVIE_MAX_LEN)
        self.start_second = min(rnd1, rnd2)
        self.end_second = max(rnd1, rnd2)

        self.current_second = self.start_second - 1

        self.key = f"{self.movie_id}_{self.user_id}"

        print(f"user {str(self.user_id)[:5]} start watch {str(self.movie_id)[:5]}")

    def continue_watch_movie(self) -> Optional[FilmViewEvent]:
        self.current_second = self.current_second + 1
        if self.current_second > self.end_second:
            print(f"user {str(self.user_id)[:5]} STOP watch {str(self.movie_id)[:5]}")
            return None

        time_now = datetime.now()
        time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")

        msg = FilmViewEvent(
            user_id=str(self.user_id), movie_id=str(self.movie_id), event_time=time_now, view_second=self.current_second
        )
        return msg
