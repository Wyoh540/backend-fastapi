from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta, last_password_change: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    now = int(datetime.now(timezone.utc).timestamp())
    to_encode = {"exp": expire, "sub": str(subject), "iat": now}
    if last_password_change is not None:
        to_encode["lpc"] = last_password_change
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
