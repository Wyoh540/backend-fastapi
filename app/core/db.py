from sqlmodel import create_engine, Session, select

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import UserManage

engine_uri = settings.SQLALCHEMY_DATABASE_URI

connection_args = {"check_same_thread": False} if "sqlite" in engine_uri else {}
engine = create_engine(engine_uri, connect_args=connection_args)


def init_db(session: Session) -> None:
    """初始化数据库，创建表格并添加默认超级用户。"""
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if not user:
        user_in = UserCreate(
            identifier=settings.FIRST_SUPERUSER,
            nickname=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        UserManage.create_user(session, user_create=user_in)
