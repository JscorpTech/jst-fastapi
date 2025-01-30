from app.db.models.news import PostModel, TagsModel, PostTagModel
from app.api.v1.schemas import news as _schema
from app.db.database import _DB


async def create_post(db: _DB, post: _schema.CreatePostSchema) -> PostModel:
    post_data = post.model_dump()
    tags = post_data.pop("tags")
    post = PostModel(**post_data)
    db.add(post)
    db.commit()
    await create_tags(db, tags, post.id)
    return post


async def create_tags(db: _DB, tags: _schema.CreateTagsSchema, post_id: int):
    for tag in tags:
        tag_instance = db.query(TagsModel).filter(TagsModel.name == tag["name"]).first()
        if not tag_instance:
            tag_instance = TagsModel(**tag)
            db.add(tag_instance)
            db.commit()
        db.add(PostTagModel(post_id=post_id, tag_id=tag_instance.id))
        db.commit()
    return tag


async def get_post(db: _DB, post_id: int) -> PostModel:
    return db.query(PostModel).filter(PostModel.id == post_id).first()


async def get_posts(db: _DB):
    return db.query(PostModel).order_by(PostModel.created_at.desc())


async def get_tags(db: _DB):
    return db.query(TagsModel)
