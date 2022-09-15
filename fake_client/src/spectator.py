from datetime import datetime
from random import randrange, getrandbits
from typing import Optional

from faker import Faker

import fake_data
from models import (
    FilmViewEvent,
    LikeEvent,
    Comment,
    Bookmark,
)

fake = Faker()


class Spectator:
    def __init__(self, user_id, movie_id, length):
        self.length = length
        self._movie_id = movie_id
        self.user_id = user_id

        self.key = None

        self.current_second = None
        self.end_second = None
        self.start_second = None

        self.start_watch_movie(length)

    @property
    def movie_id(self):
        return self._movie_id

    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = value

    def start_watch_movie(self, length):
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

        msg = FilmViewEvent(user_id=str(self.user_id),
                            movie_id=str(self.movie_id),
                            event_time=self._get_current_time(),
                            view_second=self.current_second
                            )
        return msg

    def rate_film(self) -> Optional[LikeEvent]:
        msg = LikeEvent(user_id=str(self.user_id),
                        movie_id=str(self.movie_id),
                        event_time=self._get_current_time(),
                        score=randrange(fake_data.LIKE_MAX_LEN)
                        )
        print(f"user {str(self.user_id)[:5]} rates film {str(self.movie_id)[:5]}")
        return msg

    def comment_film(self) -> Optional[Comment]:
        if not getrandbits(1):
            # рандомно не комментируем фильм
            return None

        msg = Comment(user_id=str(self.user_id),
                      movie_id=str(self.movie_id),
                      event_time=self._get_current_time(),
                      title=fake.word(),
                      body=fake.text(),
                      score=randrange(fake_data.LIKE_MAX_LEN)
                      )
        print(f"user {str(self.user_id)[:5]} comments film {str(self.movie_id)[:5]}")
        return msg

    def bookmark_film(self) -> Optional[Bookmark]:
        if not getrandbits(1):
            # рандомно не кладем фильм в закладки
            return None

        msg = Bookmark(user_id=str(self.user_id),
                       movie_id=str(self.movie_id),
                       event_time=self._get_current_time(),
                       label=fake.word(),
                       category=fake_data.CATEGORIES[randrange(fake_data.CATEGORIES_LENGTH - 1)],
                       sort_order=randrange(fake_data.SORT_ORDER_MAX_LEN)
                       )
        print(f"user {str(self.user_id)[:5]} add to bookmark film {str(self.movie_id)[:5]}")
        return msg

    @staticmethod
    def _get_current_time():
        time_now = datetime.now()
        time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
        return time_now
