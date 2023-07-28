from sqlalchemy.orm import Session

from app import schemas
from app.db import models


def like_or_dislike_post(
    post_id: int,
    db: Session,
    like: schemas.Like,
    user: schemas.User
):
    post_like = db \
                .query(models.Like) \
                .filter(
                    models.Like.post_id == post_id,
                    models.Like.user_id == user.id
                ) \
                .first()
    
    if post_like:
        post_like.like_post = like.like_post
    else:
        new_like = models.Like(
            like_post = like.like_post,
            user_id = user.id,
            post_id = post_id
        )
        db.add(new_like)
        db.commit()


def delete_like_or_dislike(
    post_id: int,
    db: Session,
    user: schemas.User
):
    db \
    .query(models.Like) \
    .filter(models.Like.post_id == post_id, models.Like.user_id == user.id) \
    .delete(synchronize_session=False)
    db.commit()