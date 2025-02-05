from typing import Optional

from fastapi import HTTPException


class APIException(HTTPException):
    VALIDATION_ERROR: str = "😰 Oops! Validation error"
    USER_NOT_FOUND: str = "🥶 User not found"
    TEMPORARY_USER_NOT_FOUND: str = "🙃 User data not found in temporary storage"
    INVALID_TOKEN: str = "🥶 Invalid token"
    INVALID_CODE: str = "🥶 Invalid code"

    def __init__(self, detail: Optional[str] = None, status_code: int = 400, data: list | dict = []) -> None:
        self.data = data
        super().__init__(status_code=status_code, detail=detail)
