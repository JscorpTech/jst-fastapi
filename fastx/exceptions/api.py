from typing import Optional

from fastapi import HTTPException


class APIException(HTTPException):
    VALIDATION_ERROR = "Oops! Validation error"

    def __init__(self, detail: Optional[str] = None, status_code: int = 400, data: list | dict = []) -> None:
        self.data = data
        super().__init__(status_code=status_code, detail=detail)
