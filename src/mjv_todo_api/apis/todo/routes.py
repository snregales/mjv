"""Todo routes."""

from typing import Iterable

from flask_restx import Resource
from flask_restx._http import HTTPStatus

from mjv_todo_api.extensions import api

from .models import Todo
from .parsers import todo_parser

ns = api.namespace("todos", description="To-Do operations")


todo_model = ns.model(
    "Todo",
    {
        key: value
        for key, value in Todo.field_descriptions()
        if key in ("id", "task", "completed", "completed_at")
    },
)


@ns.route("/")
class TodoList(Resource):
    """Shows a list of all to-dos, and lets you POST to add new tasks."""

    @ns.doc("list_todos")
    @ns.marshal_list_with(todo_model)
    def get(self) -> Iterable[Todo]:
        """List all tasks."""
        return Todo.query.all()  # type: ignore

    @ns.doc("create_todo")
    @ns.expect(todo_parser)
    @ns.marshal_with(todo_model, code=HTTPStatus.CREATED)
    def post(self) -> tuple[Todo, HTTPStatus]:
        """Create a new task."""
        return Todo.create(**todo_parser.parse_args()), HTTPStatus.CREATED


@ns.route("/<int:id>")
@ns.response(HTTPStatus.NOT_FOUND, "Todo not found")
@ns.param("id", "The task identifier")
class Task(Resource):
    """Show a single task item and lets you delete them."""

    @ns.doc("get_todo")
    @ns.marshal_with(todo_model)
    def get(self, id: int) -> Todo:
        """Fetch a given resource."""
        return Todo.query.get_or_404(id)  # type: ignore

    @ns.doc("delete_todo")
    @ns.response(HTTPStatus.NO_CONTENT, "Todo deleted")
    def delete(self, id: int) -> tuple[str, HTTPStatus]:
        """Delete a task given its identifier."""
        todo = Todo.query.get_or_404(id)
        todo.delete()
        return "", HTTPStatus.NO_CONTENT

    @ns.expect(todo_parser)
    @ns.marshal_with(todo_model)
    def put(self, id: int) -> Todo:
        """Update a task given its identifier."""
        todo = Todo.query.get_or_404(id)
        return todo.update(**todo_parser.parse_args())  # type: ignore
