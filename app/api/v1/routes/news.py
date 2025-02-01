from typing import List

from fastapi import APIRouter, Depends, Request

from app.db.database import _DB
from app.db.models import PostModel
from fastapi_core.filters import _SEARCH
from fastapi_core.manager import DBManager
from fastapi_core.pagination import _PAGE, _PAGE_SIZE, DefaultPagination
from fastapi_core.pagination import PaginationSchema as _P
from fastapi_core.response import _R

from .. import schemas as _schema
from ..services import news as _services

router = APIRouter()


@router.get("/post")
async def post(
    request: Request,
    manager: DBManager[PostModel] = Depends(PostModel.manager),
    page: _PAGE = None,
    page_size: _PAGE_SIZE = None,
    search: _SEARCH = None,
) -> _R[_P[List[_schema.ListPostSchema]]]:
    queryset = (
        manager.get_filter().filter(["title", "content"], request).search(["title", "content"], search).queryset()
    ).order_by(PostModel.created_at.desc())
    return _R(data=manager.pagination(queryset, request, page, page_size).response())


@router.post("/post")
async def create(db: _DB, post: _schema.CreatePostSchema) -> _R[_schema.ListPostSchema]:
    return _R(data=await _services.create_post(db, post))


@router.get("/post/{post_id}")
async def get_post(db: _DB, post_id: int) -> _R[_schema.ListPostSchema]:
    return _R(data=await _services.get_post(db, post_id))


@router.get("/tags")
async def tags(db: _DB, request: Request, page: _PAGE = None) -> _R[_P[List[_schema.ListTagsSchema]]]:
    return _R(data=DefaultPagination(request, page).queryset(await _services.get_tags(db)).response())
