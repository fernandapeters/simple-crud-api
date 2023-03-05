import json
import uuid

import pytest


def test_create_product_without_an_id(client):
    data = {
        "name": "test_name",
        "description": "Test description",
        "price": 3.25,
        "stock": 30
    }
    response = client.post("/products/", content=json.dumps(data))
    try:
        uuid.UUID(response.json()["id"])
    except TypeError:
        pytest.fail("Id with an invalid UUID format")
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]
    assert response.json()["stock"] == data["stock"]


def test_create_product_with_a_valid_id(client):
    data = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "test_name 2",
        "description": "Test description 2",
        "price": 0.99,
        "stock": 1500
    }
    response = client.post("/products/", content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["id"] == data["id"]
    assert response.json()["name"] == data["name"]
    assert response.json()["description"] == data["description"]
    assert response.json()["price"] == data["price"]
    assert response.json()["stock"] == data["stock"]


def test_create_product_with_an_invalid_id(client):
    data = {
        "id": "not_an_uuid",
        "name": "test_name 3",
        "description": "Test description 3",
        "price": 20.99,
        "stock": 58
    }
    response = client.post("/products/", content=json.dumps(data))
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "type_error.uuid"


def test_get_product_by_id(client):
    data = {
        "id": "53be97f1-49e2-45b4-9918-57dbe61239ce",
        "name": "product name to test",
        "description": "Product description test",
        "price": 8597.30,
        "stock": 2
    }
    post_response = client.post("/products/", content=json.dumps(data))
    assert post_response.status_code == 200

    get_response = client.get(f"/products/{data['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == data["id"]
    assert get_response.json()["name"] == data["name"]
    assert get_response.json()["description"] == data["description"]
    assert get_response.json()["price"] == data["price"]
    assert get_response.json()["stock"] == data["stock"]


def test_get_all_products(client):
    data1 = {
        "id": "53be97f1-49e2-45b4-9918-57dbe61239ce",
        "name": "product name to test",
        "description": "Product description test",
        "price": 8597.30,
        "stock": 2
    }
    post_response1 = client.post("/products/", content=json.dumps(data1))
    assert post_response1.status_code == 200

    data2 = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "test_name 2",
        "description": "Test description 2",
        "price": 0.99,
        "stock": 1500
    }
    post_response2 = client.post("/products/", content=json.dumps(data2))
    assert post_response2.status_code == 200

    get_response = client.get("/products/")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 2
    assert get_response.json()[0]["id"] == data1["id"]
    assert get_response.json()[1]["id"] == data2["id"]


def test_update_product(client):
    data = {
        "id": "53be97f1-49e2-45b4-9918-57dbe61239ce",
        "name": "product name to test",
        "description": "Product description test",
        "price": 8597.30,
        "stock": 2
    }
    post_response = client.post("/products/", content=json.dumps(data))
    assert post_response.status_code == 200

    update_data = {
        "name": "Name updated",
        "description": "Product name updated",
        "price": 1.29,
        "stock": 658
    }
    put_response = client.put(f"/products/{data['id']}", content=json.dumps(update_data))
    assert put_response.status_code == 200

    get_response = client.get(f"/products/{data['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == data["id"]
    assert get_response.json()["name"] == update_data["name"]
    assert get_response.json()["description"] == update_data["description"]
    assert get_response.json()["price"] == update_data["price"]
    assert get_response.json()["stock"] == update_data["stock"]


def test_delete_product(client):
    data = {
        "id": "53be97f1-49e2-45b4-9918-57dbe61239ce",
        "name": "product name to test",
        "description": "Product description test",
        "price": 8597.30,
        "stock": 2
    }
    post_response = client.post("/products/", content=json.dumps(data))
    assert post_response.status_code == 200

    get_response = client.get("/products/")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1

    delete_response = client.delete(f"/products/{data['id']}")
    assert delete_response.status_code == 200

    get_response = client.get("/products/")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0
