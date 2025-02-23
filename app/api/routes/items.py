from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.services.item import TagManage
from app.models import Item, Tag
from app.schemas import ItemList, ItemCreate, ItemPublic, TagList, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemList)
def get_items(session: SessionDep):
    statement = select(Item)
    items = session.exec(statement).all()
    return ItemList(data=items)


@router.post("/", response_model=ItemPublic)
def create_item(session: SessionDep, current_user: CurrentUser, item_obj: ItemCreate):

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


@router.patch("/", response_model=ItemPublic)
def update_item(session: SessionDep, current_user: CurrentUser, item_id: int, item_obj: ItemUpdate):
    db_item = session.exec(select(Item).where(Item.id == item_id)).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

    item_data = item_obj.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data, update={"owner_id": current_user.id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.get("/tags/", response_model=TagList)
def get_item_tags(session: SessionDep):
    statement = select(Tag)
    tags = session.exec(statement).all()
    return TagList(data=tags)
