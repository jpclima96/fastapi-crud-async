import json

import pytest

from app.api import crud


def test_create_event(test_app, monkeypatch):
    test_request_payload = {"name": "something", "category": "something else"}
    test_response_payload = {"id": 1, "name": "something", "category": "something else"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/events/", content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_event_invalid_json(test_app):
    response = test_app.post("/events/", content=json.dumps({"name": "something"}))
    assert response.status_code == 422

    response = test_app.post("/events/", content=json.dumps({"name": "1", "category": "2"}))
    assert response.status_code == 422


def test_read_event(test_app, monkeypatch):
    test_data = {"id": 1, "name": "something", "category": "something else"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/events/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_event_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

    response = test_app.get("/events/0")
    assert response.status_code == 422


def test_read_all_events(test_app, monkeypatch):
    test_data = [
        {"name": "something", "category": "something else", "id": 1},
        {"name": "someone", "category": "someone else", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/events/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_event(test_app, monkeypatch):
    test_update_data = {"name": "someone", "category": "someone else", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/events/1/", content=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"category": "bar"}, 422],
        [999, {"name": "foo", "category": "bar"}, 404],
        [1, {"name": "1", "category": "bar"}, 422],
        [1, {"name": "foo", "category": "1"}, 422],
        [0, {"name": "foo", "category": "bar"}, 422],
    ],
)
def test_update_event_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/events/{id}/", content=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_event(test_app, monkeypatch):
    test_data = {"name": "something", "category": "something else", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/events/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_event_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/events/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

    response = test_app.delete("/events/0/")
    assert response.status_code == 422
