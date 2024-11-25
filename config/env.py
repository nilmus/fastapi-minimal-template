import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseSettings:
    """DB_URL is the URL to connect to the database"""

    DB_URL: str


DATABASE_SETTINGS = DatabaseSettings(DB_URL=os.environ["DB_URL"])


@dataclass
class JWTSettings:
    """SECRET_KEY is the secret key used to sign the JWT token
    ALGORITHM is the algorithm used to sign the JWT token
    ACCESS_TOKEN_EXPIRE_MINUTES is the expiration time of the JWT token
    """

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


SECURITY_SETTINGS = JWTSettings(
    SECRET_KEY=os.environ["SECRET_KEY"],
    ALGORITHM=os.environ["ALGORITHM"],
    ACCESS_TOKEN_EXPIRE_MINUTES=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]),
)


@dataclass
class FrontEndSettings:
    FRONTEND_URL: str


FRONTEND_SETTINGS = FrontEndSettings(FRONTEND_URL=os.environ["FRONTEND_URL"])
