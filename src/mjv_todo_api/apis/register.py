"""Register all publically exposed namespace."""

from mjv_todo_api.extensions import api

from .todo.routes import ns as todo


def register_namespaces() -> None:
    """Initialize registered namespaces."""
    api.add_namespace(todo, path="/todo")
