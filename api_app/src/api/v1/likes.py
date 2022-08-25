from typing import Union


from api.v1.view_models import StatusMessage
from fastapi import APIRouter, Depends, Query
from models.models import Like
from services.event_service import EventService
from services.service_locator import get_event_service
from core.config import settings
import uuid

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post like event message info",
    description="Post like event message info"
)
async def like_insert(user_id: str, movie_id, like: int,
                  event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    await event_service.send_message(settings.KAFKA_FILM_LIKE_TOPIC, event_message)

    return StatusMessage(head="ok", body="all ok")


@router.get(
    '/{user_id}/',
    response_model=list[Like],
    summary="Post comment event message info",
    description="Post comment event message info"
)
async def like_list(user_id: str,
                    film_id: Union[list[str], None] = Query(default=None),
                    event_service: EventService = Depends(get_event_service)) -> list[Like]:

    # await event_service.send_message(settings.KAFKA_FILM_COMMENT_TOPIC, )
    film_items = {"q": film_id}
    tmp = [Like().random() for i in range(1, 10)]
    return tmp
