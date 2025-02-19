from sqlmodel import create_engine

from app.core.config import settings

connect_args = {"check_same_thread": False}  # 仅SQLite 配置，不同线程中使用同一个数据库
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)
