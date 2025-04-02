from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, Column, Integer
from .user import User


class ItemTagLink(SQLModel, table=True):
    """标签与物品的关联表"""

    item_id: int | None = Field(foreign_key="item.id", primary_key=True, default=None)
    tag_id: int | None = Field(foreign_key="tag.id", primary_key=True, default=None)


class Item(SQLModel, table=True):

    class StatusEnum(int, Enum):
        ONLINE = 1
        OFFLINE = 2

    id: int | None = Field(primary_key=True, default=None)
    title: str = Field(max_length=255)
    owner_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    status: StatusEnum = Field(sa_column=Column(Integer), default=StatusEnum.ONLINE)

    owner: User | None = Relationship(back_populates="items")
    tags: list["Tag"] = Relationship(back_populates="items", link_model=ItemTagLink)


class Tag(SQLModel, table=True):
    """标签表"""

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=20, index=True, unique=True)

    items: list[Item] = Relationship(back_populates="tags", link_model=ItemTagLink)
