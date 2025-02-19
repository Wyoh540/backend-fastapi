from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.models import Item
from app.schemas import ItemList, ItemCreate, ItemPublic

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemList)
def get_items(session: SessionDep, current_user: CurrentUser):
    statement = select(Item)
    items = session.exec(statement).all()
    return ItemList(data=items)


@router.post("/", response_model=ItemPublic)
def create_item(session: SessionDep, current_user: CurrentUser, item_obj: ItemCreate):
    item = Item.model_validate(item_obj, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
