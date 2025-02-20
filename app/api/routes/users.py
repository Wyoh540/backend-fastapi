from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.models import User
from app.core.security import get_password_hash
from app.api.deps import SessionDep
from app.schemas import UsersPublic, UserCreate, UserPubic
from app.task import task

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersPublic)
def get_users(session: SessionDep) -> Any:
    statement = select(User)
    users = session.exec(statement).all()
    task.hello.delay()
    return UsersPublic(data=users)


@router.post("/", response_model=UserPubic)
def create_user(session: SessionDep, user_in: UserCreate) -> Any:
    user = User(
        email=user_in.email, full_name=user_in.full_name, hashed_password=get_password_hash(user_in.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
