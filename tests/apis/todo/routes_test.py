from http import HTTPStatus
from typing import Iterator

import pytest
from flask.testing import FlaskClient


@pytest.fixture
def volitile_todos(authenticated_client: FlaskClient) -> Iterator[tuple[FlaskClient, int]]:
    """Populate database with todo that is expected to be mutated."""
    response = authenticated_client.post("/todos/", json={"task": "Initial Task"})
    todo_id = response.get_json()["id"]
    yield authenticated_client, todo_id
    authenticated_client.delete(f"/todos/{todo_id}")


def test_create_todo(volitile_todos: tuple[FlaskClient, int]) -> None:
    client, todo_id = volitile_todos
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["task"] == "Initial Task"
    assert not data["completed"]


def test_get_todos(volitile_todos: tuple[FlaskClient, int]) -> None:
    client, _ = volitile_todos
    response = client.get("/todos/")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_todo_by_id(volitile_todos: tuple[FlaskClient, int]) -> None:
    client, todo_id = volitile_todos
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["task"] == "Initial Task"


def test_update_todo(volitile_todos: tuple[FlaskClient, int]) -> None:
    client, todo_id = volitile_todos
    response = client.put(f"/todos/{todo_id}", json={"task": "Updated Task", "completed": True})
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["task"] == "Updated Task"
    assert data["completed"]


def test_delete_todo(volitile_todos: tuple[FlaskClient, int]) -> None:
    client, todo_id = volitile_todos

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
