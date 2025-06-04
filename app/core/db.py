from sqlmodel import create_engine, Session, select

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import UserManage

engine_uri = settings.SQLALCHEMY_DATABASE_URI

connection_args = {"check_same_thread": True} if "sqlite" in engine_uri else {}
engine = create_engine(engine_uri, connect_args=connection_args)


def init_db(session: Session) -> None:
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = UserManage(session).create_user(user_create=user_in)
