from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import get_password_hash


class UserManage:
    """User 管理"""

    @classmethod
    def create_user(cls, session: Session, user_create: UserCreate) -> User:
        """创建用户"""
        db_obj = User.model_validate(user_create, update={"hashed_password": get_password_hash(user_create.password)})
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @classmethod
    def update_user(cls, session: Session, db_obj: User, user_update: UserUpdate) -> User:
        """更新用户"""
        user_data = user_update.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_obj, key, value)
        if "password" in user_data:
            db_obj.hashed_password = get_password_hash(user_data["password"])
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @classmethod
    def get_user_by_username(cls, session: Session, username: str) -> User | None:
        """通过用户名获取用户"""
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    @classmethod
    def get_user_by_email(cls, session: Session, email: str) -> User | None:
        """通过邮箱获取用户"""
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()
