from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship, Field
from pydantic import EmailStr


if TYPE_CHECKING:
    from .item import Item


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    username: str = Field(max_length=255, index=True, unique=True)
    email: EmailStr | None = Field(max_length=255, index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    # cascade_delete 字段作用在Relationship上，在一对多关系的"多"侧，级联删除时使用，"一"侧的Field中需ondelete="CASCADE"
    # 如果"一"侧的Field中ondelete="SET NULL", 则cascade_delete不需要配置
    # 详细说明查看：https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
