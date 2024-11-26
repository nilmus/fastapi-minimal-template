from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from config.database import SessionDep
from models.user import User, UserCreate, UserRead, UserUpdate
from utils.auth import UserDep
from utils.models import unique_violation_handler, update_model
from utils.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(create_schema: UserCreate, session: SessionDep):
    create_schema.password = get_password_hash(create_schema.password)
    user_model = User(**create_schema.model_dump())
    with unique_violation_handler(resource_name="user"):
        session.add(user_model)
        session.commit()
        session.refresh(user_model)
        return user_model


@router.get("/me", response_model=UserRead)
def read_users_me(
    current_user: UserDep,
):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: SessionDep):
    user_model: User | None = session.get(User, user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    return user_model


@router.get("/", response_model=list[UserRead])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users: list[User] = list(
        session.execute(select(User).offset(offset).limit(limit)).scalars().all()
    )
    return users


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, update_schema: UserUpdate, session: SessionDep, current_user: UserDep
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    user: User | None = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_model(user, update_schema)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, current_user: UserDep):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return
