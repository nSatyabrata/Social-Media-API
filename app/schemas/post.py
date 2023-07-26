from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .user import User


class PostBase(BaseModel):
    title: str = None
    content: str = None
    is_public: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    owner_id: int
    user: User
    
    model_config = ConfigDict(from_attributes=True)