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
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if post_like:
        # already liked now disliking
        if post_like.like_post and not like.like_post:
            post.likes -= 1
            post.dislikes += 1
            post_like.like_post = like.like_post
        # already disliked now disliking
        elif not post_like.like_post and like.like_post:
            post.likes += 1
            post.dislikes -= 1
            post_like.like_post = like.like_post
    else:
        new_like = models.Like(
            like_post = like.like_post,
            user_id = user.id,
            post_id = post_id
        )
        if like.like_post:
            post.likes += 1
        else:
            post.dislikes += 1
        db.add(new_like)
    db.commit()


def delete_like_or_dislike(
    db: Session,
    user: schemas.User,
    liked_post: models.Like,
    post: models.Post
):
    if liked_post.like_post:
        post.likes -= 1
    else:
        post.dislikes -= 1

    db \
    .query(models.Like) \
    .filter(models.Like.post_id == post.id, models.Like.user_id == user.id) \
    .delete(synchronize_session=False)

    db.commit()