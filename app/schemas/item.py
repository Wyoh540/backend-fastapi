from sqlmodel import SQLModel, Field
from pydantic import model_serializer

from app.schemas.user import UserPublic
from app.models import ItemStatus


# Properties to receive on item creation
class ItemCreate(SQLModel):
    title: str
    tags: list[str] = []
    description: str | None = Field(default=None, max_length=1024)


# Properties to receive on item update
class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    tags: list[str] = []
    description: str | None = Field(default=None, max_length=1024)

    status: ItemStatus = Field(default=ItemStatus.ONLINE, description="1: 在线, 2: 离线")


# Properties to return to client
class ItemPublic(SQLModel):
    id: int
    title: str
    status: ItemStatus
    description: str | None = None
    owner: UserPublic
    tags: list["TagName"]


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
