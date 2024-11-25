from datetime import timedelta
from typing import Annotated

import sqlalchemy.orm as sao
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config import database as db
from config.env import SECURITY_SETTINGS
from config.security import TOKEN_URL, Token
from utils.auth import authenticate_user
from utils.security import create_access_token

router = APIRouter(
    prefix="/" + TOKEN_URL,
    tags=["token"],
)


@router.post("", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[sao.Session, Depends(db.get_session)],
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=SECURITY_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
