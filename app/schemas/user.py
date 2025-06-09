from pydantic import EmailStr
from sqlmodel import SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr | None = None
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str


# Properties to receive via API on update
class UserUpdate(SQLModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class UserPublic(SQLModel):
    id: int | None = None
    email: EmailStr | None = None
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]


class NewPassword(SQLModel):
    new_password: str
