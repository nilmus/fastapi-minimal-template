from datetime import datetime
from typing import Annotated

import pydantic as pyd
import sqlalchemy as sa
import sqlalchemy.orm as sao

from config import database as db
from config.models.user import UsernameOptions
from models.mixins import IDMixIn, TimestampMixIn
from utils.validation.user import (
    Validator,
    check_password_length,
    check_username_length,
    username_validator_factory,
)


# SqlAlchemy Model
class User(db.Base, IDMixIn, TimestampMixIn):
    """By default, username and password are required, while email is optional"""

    __tablename__ = "users"

    username: sao.Mapped[str] = sao.mapped_column(index=True, unique=True, nullable=False)
    password: sao.Mapped[str]
    email: sao.Mapped[str | None] = sao.mapped_column(
        default=None, index=True, unique=True, server_default=None, nullable=True
    )
    active: sao.Mapped[bool] = sao.mapped_column(default=True, server_default=sa.sql.true())


# Pydantic types

username_validator: Validator = username_validator_factory(UsernameOptions)

Username = Annotated[
    str, pyd.AfterValidator(username_validator), pyd.AfterValidator(check_username_length)
]
Password = Annotated[str, pyd.AfterValidator(check_password_length)]


# Pydantic Schemas
class UserBase(pyd.BaseModel):
    username: Username


class UserCreate(UserBase):
    password: Password


class UserRead(UserBase):
    id: int
    email: str | None
    active: bool
    created_at: datetime


class UserUpdate(UserBase):
    username: Username | None = None
    password: Password | None = None
    email: str | None = None
    active: bool | None = None
