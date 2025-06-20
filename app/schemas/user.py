from pydantic import EmailStr
from sqlmodel import SQLModel


# 用户信息
class UserBase(SQLModel):
    email: EmailStr | None = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str | None = None  # 密码注册时用
    auth_type: str = "password"  # 默认密码注册
    identifier: str | None = None  # 用户名/邮箱/第三方id
    credential: str | None = None  # 密码hash或第三方token


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    password: str | None = None


class NewPassword(SQLModel):
    new_password: str


class UserInDBBase(UserBase):
    id: int | None = None


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass


class UserAuthBase(SQLModel):
    auth_type: str
    identifier: str
    credential: str | None = None


class UserAuthCreate(UserAuthBase):
    user_id: int


class UserAuth(UserAuthBase):
    id: int
    user_id: int


class UserPublic(SQLModel):
    id: int | None = None
    email: EmailStr | None = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UsersPublic(SQLModel):
    data: list[UserPublic]
