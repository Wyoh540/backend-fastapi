from sqlmodel import SQLModel, Field, Relationship
from .user import User


class Item(SQLModel, table=True):

    id: int | None = Field(primary_key=True, default=None)
    title: str = Field(max_length=255)
    owner_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

    owner: User | None = Relationship(back_populates="items")
