from sqlalchemy.orm import Session

from app.db.models import Post
from app.schemas import PostCreate


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate):
    new_post = Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def update_post(db: Session, post: PostCreate, id: int):
    db.query(Post)\
        .filter(Post.id == id) \
        .update({**post.model_dump()}, synchronize_session=False)
    db.commit()
    return db.query(Post).filter(Post.id == id).first()

def delete_post(db: Session, id: int):
    db.query(Post).filter(Post.id == id).delete(synchronize_session=False)
    db.commit()