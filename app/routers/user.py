from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import db_user
from app.db import models
from app import schemas
from app.authentication.auth import get_current_user

router = APIRouter(
    tags=['Users'],
    prefix="/user"
)

@router.get('', response_model=list[schemas.User]) # authentication
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = db_user.get_users(db, skip, limit)
    return users


@router.get('/{id}', response_model=schemas.User) # authentication
def read_user(id: int, db: Session = Depends(get_db)):
    user = db_user.get_user(db, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    return user


@router.post(
    '',
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return db_user.create_user(db, user)


@router.put('/{id}', response_model=schemas.User)# authentication
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    update_user = db.query(models.User).filter(models.User.id == id).first()
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    return db_user.update_user(db, user, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)# authentication
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.id == id).first()
    if delete_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    db_user.delete_user(db, id)


@router.get('/user/me', response_model=schemas.User)
def read_user_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    return current_user