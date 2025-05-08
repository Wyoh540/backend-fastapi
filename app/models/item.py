from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, Column, Integer
from .user import User


class ItemTagLink(SQLModel, table=True):
    """标签与物品的关联表"""

    item_id: int | None = Field(foreign_key="item.id", primary_key=True, default=None)
    tag_id: int | None = Field(foreign_key="tag.id", primary_key=True, default=None)


class ItemStatus(int, Enum):
    """状态，1: 在线, 2: 离线"""

    ONLINE = 1
    OFFLINE = 2


class ItemBase(SQLModel):
    title: str = Field(max_length=255)

    status: ItemStatus = Field(
        sa_column=Column(Integer), default=ItemStatus.ONLINE.value, description="1: 在线, 2: 离线"
    )


class Item(ItemBase, table=True):
    id: int | None = Field(primary_key=True, default=None)

    # ondelete="CASCADE" 表示数据库级联删除, 在Field中使用，在一对多关系的多侧
    owner_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="items")
    tags: list["Tag"] = Relationship(back_populates="items", link_model=ItemTagLink)


class Tag(SQLModel, table=True):
    """标签表"""

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=20, index=True, unique=True)

    items: list[Item] = Relationship(back_populates="tags", link_model=ItemTagLink)
