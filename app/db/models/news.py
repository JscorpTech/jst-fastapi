from typing import Any

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastx.db import Model


class PostTagModel(Model):
    __tablename__ = "post_tags"

    id = None  # type: ignore
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class PostModel(Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title: Column[Any] = Column(JSON)
    content: Column[Any] = Column(JSON)

    tags = relationship("TagsModel", secondary="post_tags", back_populates="posts")


class TagsModel(Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name: Column[str] = Column(String(255))

    posts = relationship("PostModel", secondary="post_tags", back_populates="tags")
