"""Register all publically exposed namespace."""

from mjv.extensions import api

from .todo.routes import ns as todo
from .user.routes import ns as auth


def register_namespaces() -> None:
    """Initialize registered namespaces."""
    api.add_namespace(todo, path="/todo")
    api.add_namespace(auth, path="/auth")
