from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class MovieViewEvent(BaseModel):
    movie_id: str
    user_id: str
    event_time: datetime
    view_run_time: int


class MovieSelection(BaseModel):
    movie_id: str
    user_id: str
