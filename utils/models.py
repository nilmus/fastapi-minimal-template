"""Utility functions for models"""

import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

import pydantic as pyd
import sqlalchemy.exc as sa_exc
from fastapi import HTTPException
from psycopg2.errors import UniqueViolation

from config import database as db


def update_model(model: db.Base, update_schema: pyd.BaseModel) -> None:
    update_data = update_schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(model, key, value)


@contextmanager
def unique_violation_handler(resource_name: str | None = None) -> Generator[None, Any, None]:
    """Context manager to handle unique constraint violations.

    To be used when creating a new resource.

    Args:
        resource_name: Name of the model being created, e.g. "user"
    """
    try:
        yield
    except sa_exc.IntegrityError as e:
        resource_name = resource_name or "resource"
        if isinstance(e.orig, UniqueViolation):  # This is for Postgres
            raise HTTPException(status_code=409, detail=f"{resource_name} already exists")
        if isinstance(e.orig, sqlite3.IntegrityError):  # This is for SQLite
            raise HTTPException(status_code=409, detail=f"{resource_name} already exists")
        raise e
