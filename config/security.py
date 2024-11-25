import pydantic as pyd
from fastapi.security import OAuth2PasswordBearer

TOKEN_URL = "token"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


class Token(pyd.BaseModel):
    access_token: str
    token_type: str


class TokenData(pyd.BaseModel):
    username: str | None = None
