"""Todo routes."""

from typing import Iterable

from flask_jwt_extended import get_jwt_identity, jwt_required
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

    @jwt_required()
    @ns.doc("users_todos")
    @ns.marshal_list_with(todo_model)
    def get(self) -> Iterable[Todo]:
        """List all tasks."""
        return Todo.query.filter_by(user_id=get_jwt_identity()).all()  # type: ignore

    @jwt_required()
    @ns.doc("create_todo")
    @ns.expect(todo_parser)
    @ns.marshal_with(todo_model, code=HTTPStatus.CREATED)
    def post(self) -> tuple[Todo, HTTPStatus]:
        """Create a new task."""
        return Todo.create(
            user_id=get_jwt_identity(), **todo_parser.parse_args()
        ), HTTPStatus.CREATED


def _get_todo(id: int, user_id: int) -> Todo:
    if not (todo := Todo.query.filter_by(id=id, user_id=user_id).first()):
        ns.abort(HTTPStatus.NOT_FOUND, "Todo not found")
    return todo  # type: ignore


@ns.route("/<int:id>")
@ns.response(HTTPStatus.NOT_FOUND, "Todo not found")
@ns.param("id", "The task identifier")
class Task(Resource):
    """Show a single task item and lets you delete them."""

    @jwt_required()
    @ns.doc("get_todo")
    @ns.marshal_with(todo_model)
    def get(self, id: int) -> tuple[Todo, HTTPStatus]:
        """Fetch a given resource."""
        return _get_todo(id, get_jwt_identity()), HTTPStatus.OK

    @jwt_required()
    @ns.doc("delete_todo")
    @ns.response(HTTPStatus.NO_CONTENT, "Todo deleted")
    def delete(self, id: int) -> tuple[str, HTTPStatus]:
        """Delete a task given its identifier."""
        todo = _get_todo(id, get_jwt_identity())
        todo.delete()
        return "", HTTPStatus.NO_CONTENT

    @jwt_required()
    @ns.expect(todo_parser)
    @ns.marshal_with(todo_model)
    def put(self, id: int) -> tuple[Todo, HTTPStatus]:
        """Update a task given its identifier."""
        todo = _get_todo(id, get_jwt_identity())
        return todo.update(**todo_parser.parse_args()), HTTPStatus.OK
