from typing import Annotated, Literal

import jwt
import sqlalchemy as sa
import sqlalchemy.orm as sao
from fastapi import Depends, HTTPException, status

from config import database as db
from config.env import SECURITY_SETTINGS
from config.security import TokenData, oauth2_scheme
from models.user import User
from utils import security as sec


def get_user(session: sao.Session, username: str) -> User | None:
    return session.scalar(sa.select(User).where(User.username == username))


def authenticate_user(session: sao.Session, username: str, password: str) -> User | Literal[False]:
    user = get_user(session, username)
    if not user or not sec.verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[sao.Session, Depends(db.get_session)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SECURITY_SETTINGS.SECRET_KEY, algorithms=[SECURITY_SETTINGS.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    if token_data.username is None:
        raise credentials_exception
    user = get_user(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


UserDep = Annotated[User, Depends(get_current_active_user)]
