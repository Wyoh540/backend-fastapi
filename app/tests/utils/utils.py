import random
import string
from typing import Dict

from faker import Faker
from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_username() -> str:
    fake = Faker()
    return fake.user_name()[:10]  # Ensure username is not too long


def random_email() -> str:
    fake = Faker()
    return fake.email()


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "scope": "me items",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
