from api.v1.view_models import StatusMessage
from fastapi import APIRouter, Depends

from core.logger import logger
from models.models import EventMessage
from services.event_service import EventService
from services.service_locator import get_event_service

router = APIRouter()


@router.post("/", response_model=StatusMessage, summary="Post event message info", description="Post event message info")
async def message(event_message: EventMessage, event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    logger.info(f"send message to kafka: {event_message}")
    await event_service.send_message(event_message)
    logger.info("message has been sent successfully")
    return StatusMessage(head="ok", body="all ok")
