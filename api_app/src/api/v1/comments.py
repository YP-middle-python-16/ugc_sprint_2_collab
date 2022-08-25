from api.v1.view_models import StatusMessage
from fastapi import APIRouter, Depends
from models.models import Comment
from services.event_service import EventService
from services.service_locator import get_event_service
from core.config import settings
from api.v1.pagination_shema import PaginationSchema

router = APIRouter()


@router.get(
    '/film/{film_id}/',
    response_model=list[Comment],
    summary="list user comments",
    description="list user comments"
)
async def list_comment_by_film(film_id: str,
                               pagination: PaginationSchema = Depends(),
                               event_service: EventService = Depends(get_event_service)) -> list[Comment]:
    # await event_service.send_message(settings.KAFKA_FILM_LIKE_TOPIC, event_message)

    tmp = [Comment().random() for i in range(1, 10)]
    return tmp


@router.get(
    '/user/{user_id}/',
    response_model=list[Comment],
    summary="list user comments",
    description="list user comments"
)
async def list_comment_by_user(user_id: str,
                               pagination: PaginationSchema = Depends(),
                               event_service: EventService = Depends(get_event_service)) -> list[Comment]:
    # await event_service.send_message(settings.KAFKA_FILM_LIKE_TOPIC, event_message)

    tmp = [Comment().random() for i in range(1, 10)]
    return tmp


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post comment",
    description="Post comment"
)
async def message(comment: Comment,
                  event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    # await event_service.send_message(settings.KAFKA_FILM_COMMENT_TOPIC, event_message)

    return StatusMessage(head="ok", body="all ok")
