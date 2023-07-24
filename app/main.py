from fastapi import FastAPI

from app.db.database import engine, get_db
from app.db.models import Base
from app import routers

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routers.auth_router)
app.include_router(routers.user_router)
app.include_router(routers.post_router)

@app.get("/")
def root():
    return {"message": "Hello world"}