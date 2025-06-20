from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.models import User
from app.services.user import UserManage
from app.api.deps import SessionDep, CurrentUser, SuperUser
from app.schemas import UsersPublic, UserCreate, UserPublic, NewPassword, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersPublic)
def get_users(session: SessionDep) -> Any:
    statement = select(User)
    users = session.exec(statement).all()
    return UsersPublic(data=users)


@router.post("/", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate, current_user: SuperUser) -> Any:
    if not user_in.password:
        raise ValueError("Password is required")

    user = UserManage.create_user(session=session, user_create=user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(session: SessionDep, user_id: int, user_in: UserUpdate) -> User:
    """Update user details."""
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")

    user = UserManage.update_user(session=session, db_obj=user, user_update=user_in)

    return user


@router.delete("/{user_id}", response_model=None, status_code=204)
def delete_user(session: SessionDep, user_id: int) -> None:
    """Delete a user."""
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} not found")

    session.delete(user)
    session.commit()


@router.get("/me", response_model=UserPublic)
def get_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.patch("/me/password", response_model=UserPublic)
def reset_me_password(session: SessionDep, current_user: CurrentUser, body: NewPassword) -> Any:
    """Reset the password for the current user."""
    UserManage.change_password(session=session, user=current_user, new_password=body.new_password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
