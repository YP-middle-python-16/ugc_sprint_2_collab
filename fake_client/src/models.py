from datetime import datetime
from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmViewEvent(ORJSONModel):
    user_id: str
    movie_id: str
    event_time: datetime
    view_second: int


class EventMessage(ORJSONModel):
    key: str
    value: str


class LikeEvent(ORJSONModel):
    user_id: str
    movie_id: str
    event_time: datetime
    score: int


class Comment(ORJSONModel):
    user_id: str = None
    movie_id: str = None
    event_time: datetime = None
    title: str = None
    body: str = None
    score: int = None


class Bookmark(ORJSONModel):
    user_id: str = None
    movie_id: str = None
    label: str = None
    category: str = None
    sort_order: int = None
