from sqlmodel import SQLModel, Relationship, Field
from pydantic import EmailStr


class User(SQLModel, table=True):

    id: int | None = Field(primary_key=True, default=None)
    full_name: str | None = Field(max_length=255, default=None)
    email: EmailStr = Field(max_length=255, index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
