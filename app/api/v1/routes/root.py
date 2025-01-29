from typing import List

from fastapi import APIRouter

from fastapi_core.pagination import PaginationSchema
from fastapi_core.response import ResponseSchema

from ..schemas import RootSchema

router = APIRouter()


@router.get("/")
async def root() -> ResponseSchema[PaginationSchema[List[RootSchema]]]:
    return ResponseSchema(data=PaginationSchema(result=[RootSchema(name="root")]))
