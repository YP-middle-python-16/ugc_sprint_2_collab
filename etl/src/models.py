from datetime import datetime

from pydantic import BaseModel


class FilmViewEvent(BaseModel):
    user_id: str
    movie_id: str
    event_time: datetime
    view_second: int


class Message(BaseModel):
    topic: str
    body: FilmViewEvent
