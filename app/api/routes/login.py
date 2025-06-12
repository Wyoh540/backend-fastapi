from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.services import login
from app import schemas
from app.core.config import settings
from app.core import security

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schemas.Token:
    """
    使用用户提供的凭据（用户名和密码）进行身份验证，并生成访问令牌。

    :param session: 会话依赖，用于与数据库交互。
    :type session: SessionDep
    :param form_data: OAuth2 密码请求表单数据，包含用户名和密码。
    :type form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    :return: 包含访问令牌的响应模型。
    :rtype: schemas.Token
    """
    # 验证用户提供的凭据。
    user = login.authenticate(session=session, username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    # 设置访问令牌的过期时间。
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 生成并返回访问令牌。
    return schemas.Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expire, last_password_change=user.last_password_change
        ),
    )
