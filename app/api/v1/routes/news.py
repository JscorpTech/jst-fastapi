from typing import List

from fastapi import APIRouter, Request

from fastapi_core.pagination import DefaultPagination, PaginationSchema as _P, _PAGE, _PAGE_SIZE
from fastapi_core.response import _R
from app.db.database import _DB
from ..services import news as _services
from fastapi_core.filters import DefaultFilter, _SEARCH
from app.db.models import PostModel
from fastapi import Depends
from fastapi_core.manager import DBManager

from .. import schemas as _schema

router = APIRouter()


@router.get("/post")
async def post(
    request: Request,
    manager: DBManager = Depends(PostModel.manager),
    page: _PAGE = None,
    page_size: _PAGE_SIZE = None,
    search: _SEARCH = None,
) -> _R[_P[List[_schema.ListPostSchema]]]:
    queryset = DefaultFilter(manager.queryset()).search(["title", "content"], search)
    return _R(data=DefaultPagination(request, page, page_size).queryset(queryset).response())


@router.post("/post")
async def create(db: _DB, post: _schema.CreatePostSchema) -> _R[_schema.ListPostSchema]:
    return _R(data=await _services.create_post(db, post))


@router.get("/post/{post_id}")
async def get_post(db: _DB, post_id: int) -> _R[_schema.ListPostSchema]:
    return _R(data=await _services.get_post(db, post_id))


@router.get("/tags")
async def tags(db: _DB, request: Request, page: _PAGE = None) -> _R[_P[List[_schema.ListTagsSchema]]]:
    return _R(data=DefaultPagination(request, page).queryset(await _services.get_tags(db)).response())
