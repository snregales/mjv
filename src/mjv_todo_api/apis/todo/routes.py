"""Todo routs."""

from functools import partial
from typing import Iterable

from flask_restx import Resource
from flask_restx._http import HTTPStatus
from flask_restx.reqparse import RequestParser

from mjv_todo_api.extensions import api

from .models import Todo as TodoModel

ns = api.namespace("todos", description="To-Do operations")


todo_parser = RequestParser()
todo_parser.add_argument("task", type=str, required=True, help="Task details", location="json")
todo_parser.add_argument("completed", type=bool, help="Task completion status", location="json")

todo_model_specification = TodoModel.rest_specification(ns)
marshal_with = partial(ns.marshal_with, fields=todo_model_specification)
expect = partial(ns.expect, inputs=todo_model_specification)


@ns.route("/")
class TodoList(Resource):
    """Shows a list of all to-dos, and lets you POST to add new tasks."""

    @ns.doc("list_todos")
    @ns.marshal_list_with(todo_model_specification)
    def get(self) -> Iterable[TodoModel]:
        """List all tasks."""
        return TodoModel.query.all()  # type: ignore

    @ns.doc("create_todo")
    @expect()
    @marshal_with(code=HTTPStatus.CREATED)
    def post(self) -> tuple[TodoModel, HTTPStatus]:
        """Create a new task."""
        return TodoModel.create(**todo_parser.parse_args()), HTTPStatus.CREATED


@ns.route("/<int:id>")
@ns.response(HTTPStatus.NOT_FOUND, "Todo not found")
@ns.param("id", "The task identifier")
class Todo(Resource):
    """Show a single task item and lets you delete them."""

    @ns.doc("get_todo")
    @marshal_with()
    def get(self, id: int) -> TodoModel:
        """Fetch a given resource."""
        return TodoModel.query.get_or_404(id)  # type: ignore

    @ns.doc("delete_todo")
    @ns.response(HTTPStatus.NO_CONTENT, "Todo deleted")
    def delete(self, id: int) -> tuple[str, HTTPStatus]:
        """Delete a task given its identifier."""
        todo = TodoModel.query.get_or_404(id)
        todo.delete()
        return "", HTTPStatus.NO_CONTENT

    @expect()
    @marshal_with()
    def put(self, id: int) -> TodoModel:
        """Update a task given its identifier."""
        todo = TodoModel.query.get_or_404(id)
        return todo.update(**todo_parser.parse_args())  # type: ignore
