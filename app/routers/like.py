from fastapi import (
    APIRouter, 
    Depends, 
    status, 
    HTTPException
)
from sqlalchemy.orm import Session 

from app import schemas
from app.db.database import get_db
from app.db import db_like
from app.db import models
from app.authentication.auth import get_current_user

__all__ = ['like_router']

like_router = APIRouter(
    tags=['Like'],
    prefix='/like'
)


@like_router.post(
    '/{post_id}',
    status_code=status.HTTP_201_CREATED,
)
def like_or_dislike_post(
    post_id: int,
    like: schemas.Like,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db_like.like_or_dislike_post(post_id, db, like, current_user)


@like_router.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_like_or_dislike(
    post_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    liked_post = db \
                .query(models.Like) \
                .filter(
                    models.Like.post_id == post_id,
                    models.Like.user_id == current_user.id
                ) \
                .first()
    
    if liked_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Like or dislike not found "
                    f"for post {post_id} and user {current_user.id}")
        )
    
    db_like.delete_like_or_dislike(post_id, db, current_user)

