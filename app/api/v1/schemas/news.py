from pydantic import BaseModel
from typing import Optional
from fastapi_core.schemas.translation import TranslatedField, AutoTranslatedField


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
    title: Optional[TranslatedField] = None
    content: Optional[TranslatedField] = None


class CreatePostSchema(BasePostSchema):
    tags: list[CreateTagsSchema]


class ListPostSchema(BasePostSchema):
    id: int
    title: AutoTranslatedField
    content: AutoTranslatedField
    tags: list[ListTagsSchema]

    class Config:
        from_attributes = True
