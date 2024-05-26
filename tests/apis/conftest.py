"""Test fixtures for the API namespaces."""

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from mjv_todo_api.apis.user.models import User


@pytest.fixture(scope="module")
def new_user(app: Flask) -> User:
    """Creat a new user in the database."""
    return User.create(username="testuser", email="testuser@example.com", password="password")


@pytest.fixture
def access_token(new_user: User) -> str:
    """Create a new user with a new access token."""
    return create_access_token(identity=new_user.id)


@pytest.fixture
def authenticated_client(client: FlaskClient, access_token: str) -> FlaskClient:
    """Create user, access token and authenticate it."""
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
    return client
