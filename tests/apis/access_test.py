from http import HTTPStatus
from typing import Any

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "method, endpoint, data",
    [
        pytest.param(
            "post", "/todos/", {"task": "Test Task", "completed": False}, id="create todo"
        ),
        pytest.param("get", "/todos/", None, id="get todo list"),
        pytest.param("get", "/todos/1", None, id="get todo by id"),
        pytest.param(
            "put", "/todos/1", {"task": "Updated Task", "completed": True}, id="update a todo"
        ),
        pytest.param("delete", "/todos/1", None, id="delete todo"),
    ],
)
def test_unauthenticated_access(
    client: FlaskClient, method: str, endpoint: str, data: dict[str, Any]
) -> None:
    response = client.open(endpoint, method=method.upper(), json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
