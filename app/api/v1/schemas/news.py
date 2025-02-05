from typing import Optional

from pydantic import BaseModel

from fastx.schema.fields import _AUTOTRANSLATE, TranslatedField


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
    pass


class CreatePostSchema(BasePostSchema):
    tags: list[CreateTagsSchema]
    title: Optional[TranslatedField] = None
    content: Optional[TranslatedField] = None


class ListPostSchema(BasePostSchema):
    id: int
    title: Optional[_AUTOTRANSLATE]
    content: Optional[_AUTOTRANSLATE]
    tags: list[ListTagsSchema]

    class Config:
        from_attributes = True
