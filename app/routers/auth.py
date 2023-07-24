import os
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.authentication.auth import authenticate_user, create_access_token
from app.db.database import get_db

from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


router = APIRouter(
    tags=['Authentication'],
    prefix='/auth'
)


@router.post('/token', response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return schemas.Token(access_token=access_token, token_type="bearer")
