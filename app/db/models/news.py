from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from fastapi_core.db import Model


class PostTagModel(Model):
    __tablename__ = "post_tags"

    id = None
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class PostModel(Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title: str = Column(JSON)
    content: str = Column(JSON)

    tags = relationship("TagsModel", secondary="post_tags", back_populates="posts")


class TagsModel(Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255))

    posts = relationship("PostModel", secondary="post_tags", back_populates="tags")
