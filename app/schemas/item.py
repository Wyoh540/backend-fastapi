from sqlmodel import SQLModel
from pydantic import model_serializer

from app.schemas.user import UserPubic
from app.models import ItemBase


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str
    tags: list[str] = []


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None
    tags: list[str] = []


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str


# Properties to return to client
class ItemPublic(ItemInDBBase):
    owner: UserPubic
    tags: list["TagName"]

    # @field_serializer("tags")  # 字段序列化
    # def serialize_tags(self, tags: "TagName"):
    #     return [tag.name for tag in tags]


class ItemList(SQLModel):
    data: list[ItemPublic]


class Tag(SQLModel):
    id: int
    name: str


class TagName(SQLModel):
    name: str

    @model_serializer  # 模型序列化
    def ser_model(self) -> str:
        return self.name


class TagList(SQLModel):
    data: list[Tag] = []
