"""Utility functions for models"""

import pydantic as pyd

from config import database as db


def update_model(model: db.Base, update_schema: pyd.BaseModel) -> None:
    update_data = update_schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(model, key, value)
