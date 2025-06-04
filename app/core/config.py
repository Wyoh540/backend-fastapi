from typing import Literal, Any, Annotated
from pathlib import Path

from pydantic import AnyHttpUrl, EmailStr, AnyUrl, BeforeValidator, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "fastapi-app"
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32) 生产环境使用
    SECRET_KEY: str = "yu_muCFbLZLRlbRUdl1WVAa91JVhHl769ptqo8GhA6c"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "fastapi-app"
    SERVER_HOST: str = "http://127.0.0.1"
    FRONTEND_HOST: str = "http://localhost:3000"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)]
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]

    # sqlite: sqlite:///./sql_app.db
    # postgresql: postgresql://user:password@postgresserver/db
    # mysql: mysql+pymysql://user:password@hostname:port/db
    SQLALCHEMY_DATABASE_URI: str

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    USERS_OPEN_REGISTRATION: bool = False

    REDIS_BROKER_URL: str | None = None

    # 文件上传
    UPLOAD_DIR: Path
    MAX_FILE_SIZE: int = 1024 * 1024 * 10  # 10MB
    ALLOWED_TYPES: list[str] = ["image/jpeg", "application/pdf"]

    @field_validator("UPLOAD_DIR")
    def validate_upload_dir(cls, value: Path) -> Path:
        if not value.exists():
            value.mkdir(parents=True)
        if not value.is_dir():
            raise ValueError("Must be a directory")
        return value.resolve()


settings = Settings()
