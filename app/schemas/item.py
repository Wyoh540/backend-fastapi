from sqlmodel import SQLModel

from app.schemas.user import UserPubic


# Shared properties
class ItemBase(SQLModel):
    title: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int


# Properties to return to client
class ItemPublic(ItemInDBBase):
    owner: UserPubic


class ItemList(SQLModel):
    data: list[ItemPublic]
