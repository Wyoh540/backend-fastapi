from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import User, UserAuth
from app.schemas import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

github_oauth2 = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.GITHUB_AUTH_URL,
    tokenUrl=f"{settings.API_V1_STR}/login/github/callback",
    scopes={
        "user:email": "Read user email",
        "read:user": "Read user profile",
    },
    auto_error=False
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

# 账号密码认证依赖项
TokenDep = Annotated[str, Depends(reusable_oauth2)]

# Github OAuth2 认证依赖项
TokenDepGithub = Annotated[str, Depends(github_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep , github: TokenDepGithub) -> User:
    try:
        payload = jwt.decode(token or github, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    # 校验token签发时间与用户认证方式的last_password_change
    token_iat = token_data.iat
    auths = session.exec(select(UserAuth).where(UserAuth.user_id == user.id)).all()
    for auth in auths:
        # 只校验本地密码方式
        if auth.auth_type == "password" and auth.last_password_change and token_iat:
            if int(token_iat) < int(auth.last_password_change):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired due to password change"
                )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user


SuperUser = Annotated[User, Depends(get_current_active_superuser)]
