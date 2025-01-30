from pydantic import BaseModel
from typing import Optional


class BaseTagsSchema(BaseModel):
    name: Optional[str] = None


class CreateTagsSchema(BaseTagsSchema):
    class Config:
        from_attributes = True


class ListTagsSchema(BaseTagsSchema):
    id: int

    class Config:
        from_attributes = True


class BasePostSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class CreatePostSchema(BasePostSchema):
    tags: list[CreateTagsSchema]


class ListPostSchema(BasePostSchema):
    id: int
    tags: list[ListTagsSchema]

    class Config:
        from_attributes = True
