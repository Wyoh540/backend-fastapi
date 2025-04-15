from typing import Any

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.services.item import TagManage, ItemService
from app.models import Item, Tag
from app.filters import ItemFilter
from app.schemas import ItemCreate, ItemPublic, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=Page[ItemPublic])
def get_items(session: SessionDep, item_filter: ItemFilter = FilterDepends(ItemFilter)) -> Any:
    query = select(Item)
    query = item_filter.filter(query)
    query = item_filter.sort(query)
    return paginate(session, query)


@router.post("/", response_model=ItemPublic)
def create_item(session: SessionDep, current_user: CurrentUser, item_obj: ItemCreate) -> Any:

    # item = Item.model_validate(item_obj, update={"owner_id": current_user.id})
    item_tag_list = []
    for tag in item_obj.tags:
        tag_obj = TagManage.get_or_create_tag(db=session, tag_name=tag)
        item_tag_list.append(tag_obj)

    item = Item(**item_obj.model_dump(exclude={"tags"}), tags=item_tag_list, owner_id=current_user.id)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/{item_id}", response_model=ItemPublic)
def update_item(session: SessionDep, current_user: CurrentUser, item_id: int, item_obj: ItemUpdate) -> Any:
    db_item = ItemService.get_item_by_id(db=session, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

    item_data = item_obj.model_dump(exclude_unset=True)
    tags = item_data.pop("tags", None)
    db_item.sqlmodel_update(item_data, update={"owner_id": current_user.id})
    if tags is not None:
        item_tag_list = []
        for tag in tags:
            tag_obj = TagManage.get_or_create_tag(session, tag)
            item_tag_list.append(tag_obj)
        db_item.tags = item_tag_list
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.delete("/{item_id}", response_model=ItemPublic)
def delete_item(session: SessionDep, current_user: CurrentUser, item_id: int) -> Any:
    db_item = ItemService.get_item_by_id(db=session, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

    session.delete(db_item)
    session.commit()

    return db_item


@router.get("/tags/", response_model=list[Tag])
def get_item_tags(session: SessionDep) -> Any:
    statement = select(Tag)
    tags = session.exec(statement).all()
    return tags
