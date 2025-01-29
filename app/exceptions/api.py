from fastapi import HTTPException


class APIException(HTTPException):
    def __init__(
        self, detail: str = None, status_code: int = 400, data: list | dict = []
    ):
        self.data = data
        super().__init__(status_code=status_code, detail=detail)
