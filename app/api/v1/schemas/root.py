from pydantic import BaseModel


class RootSchema(BaseModel):
    name: str
