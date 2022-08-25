from api.v1.view_models import StatusMessage
from fastapi import APIRouter, Depends
from models.models import EventMessage, Bookmark
from services.event_service import EventService
from services.service_locator import get_event_service
from core.config import settings
from api.v1.pagination_shema import PaginationSchema

router = APIRouter()


@router.get(
    '/{user_id}',
    response_model=list[Bookmark],
    summary="List all bookmarks with pagination an optional sort and filtering",
    description=f""
)
async def bookmark_list(user_id: str,
                        pagination: PaginationSchema = Depends(),
                        event_service: EventService = Depends(get_event_service)
                        ) -> list[Bookmark]:

    tmp = [Bookmark().random() for i in range(1, 10)]
    return tmp


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post new bookmark",
    description="Post new bookmark info"
)
async def insert_bookmark(bookmark: Bookmark,
                          event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    # await event_service.send_message(settings.KAFKA_FILM_LIKE_TOPIC, event_message)

    return StatusMessage(head="ok", body="all ok")


