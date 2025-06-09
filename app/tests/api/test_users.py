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


@pytest.fixture
def user_for_test(superuser_token_headers):
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }
    create_resp = client.post(f"{API_PREFIX}/users/", json=data, headers=superuser_token_headers)
    user = create_resp.json()
    yield user  # 测试用例中可直接使用 user
    # 测试后自动删除该用户
    client.delete(f"{API_PREFIX}/users/{user['id']}", headers=superuser_token_headers)


def test_create_user(superuser_token_headers):
    data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }
    response = client.post(f"{API_PREFIX}/users/", json=data, headers=superuser_token_headers)
    assert response.status_code == 200
    user = response.json()
    try:
        assert user["username"] == data["username"]
        assert user["email"] == data["email"]
    finally:
        # 测试结束后删除该用户
        client.delete(f"{API_PREFIX}/users/{user['id']}", headers=superuser_token_headers)


def test_get_users(superuser_token_headers):
    response = client.get(f"{API_PREFIX}/users/", headers=superuser_token_headers)
    assert response.status_code == 200
    users = response.json()["data"]
    assert isinstance(users, list)


def test_update_user(superuser_token_headers, user_for_test):
    user_id = user_for_test["id"]
    update_data = {"email": fake.email()}
    response = client.patch(f"{API_PREFIX}/users/{user_id}", json=update_data, headers=superuser_token_headers)
    assert response.status_code == 200
    # 用户名未变，邮箱已更新
    assert response.json()["email"] == update_data["email"]
    assert response.json()["username"] == user_for_test["username"]


def test_get_me(superuser_token_headers):
    response = client.get(f"{API_PREFIX}/users/me", headers=superuser_token_headers)
    assert response.status_code == 200
    assert "username" in response.json()


def test_delete_user(superuser_token_headers, user_for_test):
    user_id = user_for_test['id']
    response = client.delete(f"{API_PREFIX}/users/{user_id}", headers=superuser_token_headers)
    assert response.status_code == 204
