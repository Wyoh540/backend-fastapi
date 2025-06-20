from typing import Annotated, Any
from datetime import timedelta

from fastapi import APIRouter, Depends, status, Form
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
import httpx

from app.api.deps import SessionDep
from app.models import user as user_model
from app.services.user import UserManage
from sqlmodel import select
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
    """
    # 通过UserAuth表认证
    auth = session.exec(
        select(user_model.UserAuth).where(
            user_model.UserAuth.auth_type == "password", user_model.UserAuth.identifier == form_data.username
        )
    ).first()
    if not auth or not security.verify_password(form_data.password, auth.credential):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    user = session.get(user_model.User, auth.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expire, last_password_change=auth.last_password_change
        ),
    )


@router.get("/github-login")
def github_login(redirect_uri: str = Form(...)) -> Any:
    """请求Github认证"""
    github_auth_url = (
        f"{settings.GITHUB_AUTH_URL}?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}&scope=read:user user:email"
    )
    return RedirectResponse(github_auth_url)


@router.post("/github/callback")
async def github_callback(session: SessionDep, code: str = Form(...), redirect_uri: str = Form(...)) -> Any:
    """获取访问令牌并处理用户信息"""
    if not code:
        return JSONResponse(status_code=400, content={"detail": "Missing code from GitHub callback"})
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": redirect_uri,
            },
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return JSONResponse(status_code=400, content={"detail": "Failed to get GitHub access token"})
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"},
        )
        user_data = user_resp.json()
        github_id = user_data.get("id")
        github_email = user_data.get("email")
        github_login = user_data.get("login")
        if not github_id:
            return JSONResponse(status_code=400, content={"detail": "Failed to get GitHub user info"})
        user = None
        if github_email:
            user = UserManage.get_user_by_email(session, github_email)
        if not user:
            auth = session.exec(
                select(user_model.UserAuth).where(
                    user_model.UserAuth.auth_type == "github", user_model.UserAuth.identifier == str(github_id)
                )
            ).first()
            if auth:
                user = session.get(user_model.User, auth.user_id)
        if not user:
            from app.schemas.user import UserCreate
            reg_nickname = github_login or f"github_{github_id}"
            user_in = UserCreate(
                nickname=reg_nickname,
                email=github_email,
                auth_type="github",
                identifier=str(github_id),
                credential=access_token,
            )
            user = UserManage.create_user(session, user_in)
            auth = session.exec(
                select(user_model.UserAuth).where(
                    user_model.UserAuth.user_id == user.id, user_model.UserAuth.auth_type == "github"
                )
            ).first()
        else:
            auth = session.exec(
                select(user_model.UserAuth).where(
                    user_model.UserAuth.user_id == user.id, user_model.UserAuth.auth_type == "github"
                )
            ).first()
            if not auth:
                auth = user_model.UserAuth(
                    user_id=user.id,
                    auth_type="github",
                    identifier=str(github_id),
                    credential=access_token,
                )
                session.add(auth)
                session.commit()
        access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        jwt_token = security.create_access_token(
            user.id,
            expires_delta=access_token_expire,
            last_password_change=(auth.last_password_change if auth else None),
        )
        return schemas.Token(access_token=jwt_token)
