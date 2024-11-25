from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from config.env import SECURITY_SETTINGS


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_pw.encode())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECURITY_SETTINGS.SECRET_KEY, algorithm=SECURITY_SETTINGS.ALGORITHM
    )
    return encoded_jwt
