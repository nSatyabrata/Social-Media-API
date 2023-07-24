from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    new_user = User()
    new_user.username = user.username
    new_user.hashed_password = user.password # hashed it
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user: UserCreate, id: int):
    db.query(User)\
        .filter(User.id == id) \
        .update({**user.model_dump()}, synchronize_session=False)
    db.commit()

    # based on hashed password
    return db.query(User).filter(User.id == id).first()

def delete_user(db: Session, id: int):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()