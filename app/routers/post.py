from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import db_post
from app.db import models
from app.authentication.auth import get_current_user
from app.db.database import get_db


__all__ = ['post_router']

post_router = APIRouter(
    tags=['Posts'],
    prefix="/post"
)

@post_router.get('', response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    posts = db_post.get_posts(db, skip, limit)
    return posts


@post_router.get('/my', response_model=list[schemas.Post])
def read_my_posts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_post.get_my_posts(db, current_user)


@post_router.get('/{id}', response_model=schemas.Post)
def read_post(id: int, db: Session = Depends(get_db)):
    post = db_post.get_post(db, id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@post_router.post(
    '',
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED
)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_post.create_post(db, post, current_user)


@post_router.put('/{id}', response_model=schemas.Post)
def update_post(
    id: int, 
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    update_post = db.query(models.Post).filter(models.Post.id == id).first()
    if update_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return db_post.update_post(db, post, id, current_user)


@post_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_post = db.query(models.Post)\
                    .filter(
                        models.Post.id == id, 
                        models.Post.owner_id == current_user.id
                    ).first()
    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    db_post.delete_post(db, id, current_user)
