from pydantic import BaseModel


class Like(BaseModel):
    like_post : bool
