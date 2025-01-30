from pydantic import BaseModel as PyBaseModel
from fastapi_core.exceptions import APIException


__all__ = [
    "BaseModel",
]


class BaseModel(PyBaseModel):
    async def is_valid(self, fields: list[str] = None, raise_exception: bool = False):
        fields = fields or [func.replace("validate_", "") for func in dir(self) if func.startswith("validate_")]
        result = {}
        errors = {}
        for field in fields:
            field_call = "validate_%s" % field
            if hasattr(self, field_call):
                try:
                    result[field] = await getattr(self, field_call)(getattr(self, field))
                except ValueError as e:
                    if not raise_exception:
                        raise e
                    errors[field] = e
        if len(errors) > 0:
            raise APIException(data=[{key: str(e)} for key, e in errors.items()])
        return result
