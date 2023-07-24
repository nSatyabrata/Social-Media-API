from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str = None
    content: str = None
    public: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    
    model_config = ConfigDict(from_attributes=True)