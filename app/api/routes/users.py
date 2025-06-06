from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.models import User
from app.core.security import get_password_hash
from app.api.deps import SessionDep, CurrentUser
from app.schemas import UsersPublic, UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersPublic)
def get_users(session: SessionDep) -> Any:
    statement = select(User)
    users = session.exec(statement).all()
    return UsersPublic(data=users)


@router.post("/", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate) -> Any:
    user = User(email=user_in.email, username=user_in.username, hashed_password=get_password_hash(user_in.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/me", response_model=UserPublic)
def get_user_me(current_user: CurrentUser) -> Any:
    return current_user
