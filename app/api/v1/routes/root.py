from fastapi import APIRouter
from fastx.storage import default_storage


router = APIRouter()


@router.get("/")
async def root() -> dict:
    detail: str = default_storage().read("test.txt")
    return {"detail": detail}
