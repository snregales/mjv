"""App module."""

from flask import Flask

from .apis.register import register_namespaces
from .extensions import api, bcrypt, db, jwt


def create_app(config_object: str | object = "mjv_todo_api.settings") -> Flask:
    """Create application factory.

    As explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_namespaces()
    return app


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
