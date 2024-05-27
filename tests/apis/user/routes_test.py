from http import HTTPStatus

from flask.testing import FlaskClient

from mjv.apis.user.models import User


def test_register_existing_user(client: FlaskClient, new_user: User) -> None:
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "testuser@example.com", "password": "password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register(client: FlaskClient) -> None:
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "password"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json()["username"] == "testuser2"
    assert response.get_json()["email"] == "testuser2@example.com"


def test_login(client: FlaskClient, new_user: User) -> None:
    response = client.post(
        "/auth/login", json={"username": new_user.username, "password": "password"}
    )
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.get_json()


def test_current_user(authenticated_client: FlaskClient) -> None:
    response = authenticated_client.get("/auth/current_user")
    assert response.status_code == HTTPStatus.OK
    user_data = response.get_json()
    assert user_data["username"] == "testuser"
    assert user_data["email"] == "testuser@example.com"


def test_change_password(authenticated_client: FlaskClient) -> None:
    response = authenticated_client.put(
        "/auth/current_user", json={"old_password": "password", "new_password": "newpassword"}
    )
    assert response.status_code == HTTPStatus.OK
    user_data = response.get_json()
    assert user_data["username"] == "testuser"
    assert user_data["email"] == "testuser@example.com"
