from sqlmodel import Session, select
from fastapi import HTTPException

from app.models import Tag, Item


class TagManage:
    """Tag 管理"""

    @classmethod
    def get_or_create_tag(cls, db: Session, tag_name: str) -> Tag:
        """Get or create a tag by name."""
        existing_tag = db.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not existing_tag:
            new_tag = Tag(name=tag_name)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)

            existing_tag = new_tag
        return existing_tag


class ItemService:
    """Item 服务"""

    @classmethod
    def get_item_by_id(cla, db: Session, item_id: int) -> Item:
        """获取Item"""
        db_item = db.get(Item, item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item
