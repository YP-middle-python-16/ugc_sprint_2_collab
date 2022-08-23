from api.v1.view_models import StatusMessage
from fastapi import APIRouter, Depends
from models.models import EventMessage
from services.event_service import EventService
from services.service_locator import get_event_service
from core.config import settings

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post view event message info",
    description="Post view event message info"
)
async def message(event_message: EventMessage,
                  event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    await event_service.send_message(settings.KAFKA_FILM_VIEW_TOPIC, event_message)

    return StatusMessage(head="ok", body="all ok")


@router.post(
    '/like/',
    response_model=StatusMessage,
    summary="Post like event message info",
    description="Post like event message info"
)
async def message(event_message: EventMessage,
                  event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    await event_service.send_message(settings.KAFKA_FILM_LIKE_TOPIC, event_message)

    return StatusMessage(head="ok", body="all ok")



@router.post(
    '/comment/',
    response_model=StatusMessage,
    summary="Post comment event message info",
    description="Post comment event message info"
)
async def message(event_message: EventMessage,
                  event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    await event_service.send_message(settings.KAFKA_FILM_COMMENT_TOPIC, event_message)

    return StatusMessage(head="ok", body="all ok")

