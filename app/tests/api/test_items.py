import pytest
from fastapi.testclient import TestClient

from app.tests.utils.utils import random_lower_string
from app.core.config import settings


API_PREFIX = settings.API_V1_STR


@pytest.fixture
def item_data():
    return {
        "title": random_lower_string(8),
        "description": random_lower_string(16),
        "tags": [random_lower_string(5), random_lower_string(5)],
    }


def test_get_items(client: TestClient, superuser_token_headers):
    response = client.get(f"{API_PREFIX}/items/", headers=superuser_token_headers)
    assert response.status_code == 200
    assert "items" in response.json()


def test_create_item(client: TestClient, superuser_token_headers, item_data):
    response = client.post(f"{API_PREFIX}/items/", json=item_data, headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert set(data["tags"]) == set(item_data["tags"])
    assert "id" in data


def test_update_item(client: TestClient, superuser_token_headers, item_data):
    # 先创建一个item
    create_resp = client.post(f"{API_PREFIX}/items/", json=item_data, headers=superuser_token_headers)
    item_id = create_resp.json()["id"]
    update_data = {"title": random_lower_string(10), "tags": [random_lower_string(5)]}
    response = client.patch(f"{API_PREFIX}/items/{item_id}", json=update_data, headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert set(data["tags"]) == set(update_data["tags"])


def test_delete_item(client: TestClient, superuser_token_headers, item_data):
    create_resp = client.post(f"{API_PREFIX}/items/", json=item_data, headers=superuser_token_headers)
    item_id = create_resp.json()["id"]
    response = client.delete(f"{API_PREFIX}/items/{item_id}", headers=superuser_token_headers)
    assert response.status_code == 200
    # 再次获取应为404
    get_resp = client.patch(f"{API_PREFIX}/items/{item_id}", json={"title": "x"}, headers=superuser_token_headers)
    assert get_resp.status_code == 404


def test_get_item_tags(client: TestClient, superuser_token_headers):
    response = client.get(f"{API_PREFIX}/items/tags/", headers=superuser_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
