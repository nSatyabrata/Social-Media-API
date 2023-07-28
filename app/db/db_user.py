from sqlalchemy.orm import Session

from app.db import models
from app.schemas import UserCreate, UserUpdate
from app.authentication.auth import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    new_user = models.User()
    new_user.username = user.username
    new_user.hashed_password = get_password_hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user: UserUpdate, id: int):
    to_update_user = db.query(models.User).filter(models.User.id == id).first()
    if user.username:
        to_update_user.username = user.username
    
    if user.password:
        to_update_user.hashed_password = get_password_hash(user.password)
    
    db.commit()


def delete_user(db: Session, id: int):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()