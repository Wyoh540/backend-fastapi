from sqlmodel import create_engine, Session, select

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import UserManage

connect_args = {"check_same_thread": False}  # 仅SQLite 配置，不同线程中使用同一个数据库
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)


def init_db(session: Session) -> None:

    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = UserManage(session).create_user(user_create=user_in)
