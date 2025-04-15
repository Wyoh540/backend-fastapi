from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models import Item


class ItemFilter(Filter):
    order_by: list[str] | None = Field(
        Query(default=None, description="多个字段使用`,`隔开，字段前`-`表示降序， 例如 `-id` 表示降序")
    )
    status: Item.StatusEnum | None = Field(Query(default=None, description="1: 在线， 2: 离线"))
    title__like: str | None = None

    class Constants(Filter.Constants):
        model = Item
