from flask import Flask

from mjv.extensions import api, db


def test_app_factory(app: Flask) -> None:
    assert app is not None
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_database_initialization(app: Flask) -> None:
    with app.app_context():
        assert db.engine is not None
        assert db.session is not None


def test_namespace_registration(app: Flask) -> None:
    with app.app_context():
        registered_namespaces = [namespace.name for namespace in api.namespaces]
        assert "todos" in registered_namespaces, "Namespace 'todos' not registered correctly"
