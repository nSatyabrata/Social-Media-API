from sqlalchemy.orm import Session

from app.db.models import Post
from app import schemas


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id, Post.is_public == True).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).filter(Post.is_public == True).offset(skip).limit(limit).all()


def get_my_posts(db: Session, owner: schemas.User):
    return db.query(Post).filter(Post.owner_id == owner.id).all()


def create_post(db: Session, post: schemas.PostCreate, owner: schemas.User):
    new_post = Post(
        title=post.title,
        content=post.content,
        is_public=post.is_public,
        owner_id=owner.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def update_post(db: Session, post: schemas.PostCreate, id: int, owner: schemas.User):
    db.query(Post)\
        .filter(Post.id == id, Post.owner_id == owner.id) \
        .update({**post.model_dump()}, synchronize_session=False)
    db.commit()
    return db.query(Post).filter(Post.id == id).first()

def delete_post(db: Session, id: int, owner: schemas.User):
    db.query(Post).filter(Post.id == id, Post.owner_id == owner.id).delete(synchronize_session=False)
    db.commit()