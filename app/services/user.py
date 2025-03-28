from sqlmodel import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash


class UserManage:
    """User 管理"""

    def __init__(self, session: Session):
        self.db = session

    def create_user(self, user_create: UserCreate) -> User:
        """创建用户"""
        db_obj = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
