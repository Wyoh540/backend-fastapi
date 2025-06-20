from datetime import datetime
from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User, UserAuth
from app.core.security import get_password_hash


class UserManage:
    """User 管理"""

    @classmethod
    def create_user(cls, session: Session, user_create: UserCreate) -> User:
        """创建用户（含认证信息）"""
        db_user = User(
            nickname=user_create.nickname,
            email=user_create.email,
            is_active=True,
            is_superuser=user_create.is_superuser,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        print(db_user)
        # 创建认证方式
        credential = user_create.credential or (
            get_password_hash(user_create.password) if user_create.password else None
        )
        db_auth = UserAuth(
            user_id=db_user.id,
            auth_type=user_create.auth_type,
            identifier=user_create.identifier,
            credential=credential,
        )
        session.add(db_auth)
        session.commit()
        return db_user

    @classmethod
    def update_user(cls, session: Session, db_obj: User, user_update: UserUpdate) -> User:
        """更新用户"""
        user_data = user_update.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @classmethod
    def change_password(cls, session: Session, user: User, new_password: str) -> None:
        """变更本地密码认证方式的密码，并更新时间戳"""
        # 查找本地password认证方式
        auth = session.exec(
            select(UserAuth).where(UserAuth.user_id == user.id, UserAuth.auth_type == "password")
        ).first()
        if auth:
            auth.credential = get_password_hash(new_password)
            auth.last_password_change = int(datetime.now().timestamp())
            session.add(auth)
            session.commit()

    @classmethod
    def get_user_by_auth(cls, session: Session, auth_type: str, identifier: str) -> User | None:
        """通过认证信息获取用户"""
        statement = select(UserAuth).where(UserAuth.auth_type == auth_type, UserAuth.identifier == identifier)
        auth = session.exec(statement).first()
        if auth:
            return session.get(User, auth.user_id)
        return None

    @classmethod
    def get_user_by_email(cls, session: Session, email: str) -> User | None:
        """通过邮箱获取用户"""
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()
