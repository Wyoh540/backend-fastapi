from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Relationship, Field
from pydantic import EmailStr


if TYPE_CHECKING:
    from .item import Item


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    nickname: str | None = Field(max_length=255, index=True)
    email: EmailStr | None = Field(max_length=255, index=True, unique=True)
    avatar: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    auths: list["UserAuth"] = Relationship(back_populates="user")
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


class UserAuth(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id")
    auth_type: str = Field(max_length=32, index=True)  # 'password', 'github', 'wechat', etc.
    identifier: str = Field(max_length=255, index=True)  # username/email/openid/github_id等
    credential: str  # 密码hash或第三方token等
    last_password_change: int | None = Field(default=None, description="上次密码修改时间戳，仅password方式用")
    user: Optional[User] = Relationship(back_populates="auths")
