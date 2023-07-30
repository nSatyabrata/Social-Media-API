from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.models import Base
from app import routers

#Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.auth_router)
app.include_router(routers.user_router)
app.include_router(routers.post_router)
app.include_router(routers.like_router)

@app.get("/")
def root():
    return {"message": "Hello  User. Login and enjoy..."}