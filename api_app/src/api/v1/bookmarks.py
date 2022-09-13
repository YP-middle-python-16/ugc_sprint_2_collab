import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.view_models import StatusMessage
from models.models import Bookmark
from services.doc_service import DocService
from services.service_locator import get_storage_service
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
                        storage_service: DocService = Depends(get_storage_service)
                        ) -> list[Bookmark]:
    queue = {'user_id': user_id}
    queue_json = json.dumps(queue, indent=4)
    bookmarks = await storage_service.select(queue_json, settings.MONGO_TABLE_LIKE)

    if len(bookmarks) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    start = (pagination.page_number - 1) * pagination.page_size
    end = start + pagination.page_size

    return bookmarks[start:end]


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post new bookmark",
    description="Post new bookmark info"
)
async def insert_bookmark(bookmark: Bookmark,
                          storage_service: DocService = Depends(get_storage_service)) -> StatusMessage:
    bookmark = dict(bookmark)
    await storage_service.insert(bookmark, settings.MONGO_TABLE_BOOKMARK)

    return StatusMessage(head="ok", body="all ok")
