import uuid
from datetime import datetime
from random import randrange, choice

from pydantic import BaseModel

from models.utils import write_comment, random_date


class MovieViewEvent(BaseModel):
    movie_id: str
    user_id: str
    event_time: datetime
    view_run_time: int


class MovieSelection(BaseModel):
    movie_id: str
    user_id: str


class Comment(BaseModel):
    user_id: str = None
    movie_id: str = None
    event_time: datetime = None
    title: str = None
    body: str = None
    score: int = None

    @staticmethod
    def random():
        user_id = str(uuid.uuid4())
        movie_id = str(uuid.uuid4())

        d1 = datetime.strptime('1/1/2019 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')

        event_time = random_date(d1, d2)
        title = write_comment("{so|totally|i like|totaly bad|very good}")
        body = write_comment("{{so|totally} ugly|very {nice|bad}} {photo|media|upload} {:)||:D|<3}")
        score = choice([-1, 0, 1])
        return Comment(user_id=user_id,
                       movie_id=movie_id,
                       event_time=event_time,
                       title=title,
                       body=body,
                       score=score)


class EventMessage(BaseModel):
    key: str
    value: str


class Bookmark(BaseModel):
    user_id: str = None
    movie_id: str = None
    label: str = None
    category: str = None
    sort_order: int = None

    @staticmethod
    def random():
        user_id = str(uuid.uuid4())
        movie_id = str(uuid.uuid4())
        category = write_comment("{so|totally|i like|totaly bad|very good}")
        label = write_comment("{{so|totally} ugly|very {nice|bad}} {photo|media|upload} {:)||:D|<3}")
        sort_order = randrange(1, 1000)

        return Bookmark(user_id=user_id,
                        movie_id=movie_id,
                        category=category,
                        label=label,
                        sort_order=sort_order)


class Like(BaseModel):
    movie_id: str = None
    count: int = None
    user_liked: bool = None

    @staticmethod
    def random():
        movie_id = str(uuid.uuid4())
        count = randrange(1, 1000)
        user_liked = True if (randrange(1, 1000) > 500) else False
        return Like(movie_id=movie_id, count=count, user_liked=user_liked)
