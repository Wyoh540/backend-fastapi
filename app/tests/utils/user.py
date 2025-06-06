from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.services.user import UserManage
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(*, client: TestClient, username: str, password: str, scope: str) -> Dict[str, str]:
    data = {"username": username, "password": password, "scope": scope}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    """生成随机用户

    Args:
        db (Session): 数据库会话

    Returns:
        User: 用户实例
    """

    username = random_lower_string(length=5)
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=username, email=email, password=password)
    user = UserManage.create_user(session=db, user_create=user_in)
    return user


def authentication_token_from_username(*, client: TestClient, username: str, db: Session) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = UserManage.get_user_by_username(session=db, username=username)
    if not user:
        user_in_create = UserCreate(username=username, password=password)
        user = UserManage.create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = UserManage.update_user(session=db, db_obj=user, user_update=user_in_update)

    return user_authentication_headers(client=client, username=username, password=password, scope="")
