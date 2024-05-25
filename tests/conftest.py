"""Package test Configuration."""

from typing import Iterator

import pytest
import werkzeug
from click.testing import CliRunner
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm.session import Session

from mjv_todo_api.app import create_app
from mjv_todo_api.database import Model, PkModel
from mjv_todo_api.extensions import db


class TestConfig:
    """Test Configuration."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class CRUDMixinModel(Model):
    """CRUD Mixin Model."""

    __tablename__ = "crud_mixin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class PkModelTest(PkModel):
    """primary key Model."""

    __tablename__ = "pk_model_test"
    name = db.Column(db.String(50))


@pytest.fixture(scope="module")
def crud_model() -> type[Model]:
    """CRUDMixinModel class."""
    return CRUDMixinModel


@pytest.fixture(scope="module")
def pk_model() -> type[PkModel]:
    """PkModel class."""
    return PkModelTest


@pytest.fixture(scope="module")
def app() -> Iterator[Flask]:
    """Fixture to create and configure the Flask app.

    Returns:
        Flask: The Flask application instance.
    """
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="module")
def client(app: Flask) -> FlaskClient:
    """Fixture to provide a test client for the app.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskClient: The test client for the Flask application.
    """
    return app.test_client()


@pytest.fixture
def session(app: Flask) -> Iterator[Session]:
    """Fixture to handle database session with automatic rollback after each test.

    Args:
        app (Flask): The Flask application instance.

    Yields:
        Session: The SQLAlchemy session instance.
    """
    with app.app_context():
        db.session.begin(nested=True)
        yield db.session  # type:ignore
        db.session.rollback()


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def create_shutdown_route(app: Flask) -> None:
    """Create a shutdown route in the Flask app for testing purposes."""

    @app.route("/shutdown", methods=["POST"])
    def _() -> str:
        werkzeug.server.shutdown()
        return "Server shutting down..."


@pytest.fixture(scope="module", autouse=True)
def add_shutdown_route(app: Flask) -> Iterator[None]:
    """Add a shutdown route to Flask test app."""
    create_shutdown_route(app)
    yield
