import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from faker import Faker

client = TestClient(app)
API_PREFIX = settings.API_V1_STR
fake = Faker()


@pytest.fixture
def superuser_token_headers():
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "scope": "me users",
    }
    r = client.post(f"{API_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def test_create_user(superuser_token_headers):
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }
    response = client.post(f"{API_PREFIX}/users/", json=data, headers=superuser_token_headers)
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == data["username"]
    assert user["email"] == data["email"]


def test_get_users(superuser_token_headers):
    response = client.get(f"{API_PREFIX}/users/", headers=superuser_token_headers)
    assert response.status_code == 200
    users = response.json()["data"]
    assert isinstance(users, list)


def test_update_user(superuser_token_headers):
    # 先创建用户
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }
    create_resp = client.post(f"{API_PREFIX}/users/", json=data, headers=superuser_token_headers)
    user_id = create_resp.json()["id"]
    update_data = {"username": fake.user_name()}
    response = client.patch(f"{API_PREFIX}/users/{user_id}", json=update_data, headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json()["username"] == update_data["username"]


def test_get_me(superuser_token_headers):
    response = client.get(f"{API_PREFIX}/users/me", headers=superuser_token_headers)
    assert response.status_code == 200
    assert "username" in response.json()
