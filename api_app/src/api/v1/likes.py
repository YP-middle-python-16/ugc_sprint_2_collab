from typing import Union
import json

from datetime import datetime

from api.v1.view_models import StatusMessage
from fastapi import APIRouter, Depends, Query
from models.models import Like, LikeEvent
from services.doc_service import DocService
from services.service_locator import get_storage_service
from core.config import settings

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post like event message info",
    description="Post like event message info"
)
async def like_insert(user_id: str, movie_id, like: int,
                      storage_service: DocService = Depends(get_storage_service)) -> StatusMessage:
    new_like = LikeEvent(user_id=user_id,
                         movie_id=movie_id,
                         event_time=datetime.now(),
                         score=like)

    new_like = dict(new_like)
    await storage_service.insert(new_like, settings.MONGO_TABLE_LIKE)
    return StatusMessage(head="ok", body="all ok")


@router.get(
    '/{user_id}/',
    response_model=list[Like],
    summary="Post comment event message info",
    description="Post comment event message info"
)
async def like_list(user_id: str,
                    movie_ids: Union[list[str], None] = Query(default=None),
                    storage_service: DocService = Depends(get_storage_service)) -> list[Like]:
    likes = []

    for movie_id in movie_ids:
        film_queue = {'movie_id': movie_id}
        film_queue_json = json.dumps(film_queue, indent=4)
        like_count = await storage_service.count(film_queue_json, settings.MONGO_TABLE_LIKE)

        user_queue = {
            'movie_id': movie_id,
            'user_id': user_id
        }
        user_queue_json = json.dumps(user_queue, indent=4)
        user_like_count = await storage_service.count(user_queue_json, settings.MONGO_TABLE_LIKE)
        user_liked = False
        if user_like_count > 0:
            user_liked = True

        like = Like(
            movie_id=movie_id,
            count=like_count,
            user_liked=user_liked
        )

        likes.append(like)

    return likes
