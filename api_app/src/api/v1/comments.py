import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.view_models import StatusMessage
from models.models import Comment
from services.doc_service import DocService
from services.service_locator import get_storage_service
from core.config import settings
from api.v1.pagination_shema import PaginationSchema

router = APIRouter()


@router.get(
    '/film/{film_id}/',
    response_model=list[Comment],
    summary="list user comments",
    description="list user comments"
)
async def list_comment_by_film(movie_id: str,
                               pagination: PaginationSchema = Depends(),
                               storage_service: DocService = Depends(get_storage_service)) -> list[Comment]:
    queue = {'movie_id': movie_id}
    queue_json = json.dumps(queue, indent=4)
    comments = await storage_service.select(queue_json, settings.MONGO_TABLE_LIKE)

    if len(comments) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='comment not found')

    start = (pagination.page_number - 1) * pagination.page_size
    end = start + pagination.page_size

    return comments[start:end]


@router.get(
    '/user/{user_id}/',
    response_model=list[Comment],
    summary="list user comments",
    description="list user comments"
)
async def list_comment_by_user(user_id: str,
                               pagination: PaginationSchema = Depends(),
                               storage_service: DocService = Depends(get_storage_service)) -> list[Comment]:
    queue = {'user_id': user_id}
    queue_json = json.dumps(queue, indent=4)
    comments = await storage_service.select(queue_json, settings.MONGO_TABLE_LIKE)

    if len(comments) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='comment not found')

    start = (pagination.page_number - 1) * pagination.page_size
    end = start + pagination.page_size

    return comments[start:end]


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post comment",
    description="Post comment"
)
async def post_comment(comment: Comment,
                       storage_service: DocService = Depends(get_storage_service)) -> StatusMessage:
    comment = dict(comment)
    await storage_service.insert(comment, settings.MONGO_TABLE_COMMENT)

    return StatusMessage(head="ok", body="all ok")
