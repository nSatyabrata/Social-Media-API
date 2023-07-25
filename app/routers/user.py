from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.db import db_user
from app.db import models
from app.db.database import get_db
from app.authentication.auth import get_current_user


__all__ = ['user_router']

user_router = APIRouter(
    tags=['Users'],
    prefix="/user"
)


@user_router.post(
    '',
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    return db_user.create_user(db, user)


@user_router.get('/me', response_model=schemas.User)
def read_user_me(
    current_user: schemas.User = Depends(get_current_user)
):
    return current_user


@user_router.get('/all', response_model=list[schemas.User]) # authentication
def read_users(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user)
):  
    if current_user:
        users = db_user.get_users(db, skip, limit)
        return users


@user_router.get('/{id}', response_model=schemas.User) # authentication
def read_user(
    id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    user = db_user.get_user(db, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    return user


@user_router.put('', status_code=status.HTTP_204_NO_CONTENT)
def update_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    update_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    db_user.update_user(db, user, update_user.id)


@user_router.delete('', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    #id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    delete_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    db_user.delete_user(db, delete_user.id)