"""App module."""

from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version="1.0", title="To-Do API", description="A simple To-Do API")

ns = api.namespace("todos", description="To-Do operations")

# In-memory storage for to-do items
todos = []
next_id = 1

# Define the model for input and output
todo_model = api.model(
    "Todo",
    {
        "id": fields.Integer(readOnly=True, description="The unique identifier of a task"),
        "task": fields.String(required=True, description="The task details"),
        "completed": fields.Boolean(description="Task completion status"),
    },
)

todo_parser = api.parser()
todo_parser.add_argument("task", type=str, required=True, help="Task details", location="json")
todo_parser.add_argument("completed", type=bool, help="Task completion status", location="json")


@ns.route("/")
class TodoList(Resource):
    """Shows a list of all to-dos, and lets you POST to add new tasks."""

    @ns.doc("list_todos")
    @ns.marshal_list_with(todo_model)
    def get(self):
        """List all tasks."""
        return todos

    @ns.doc("create_todo")
    @ns.expect(todo_model)
    @ns.marshal_with(todo_model, code=201)
    def post(self):
        """Create a new task."""
        global next_id
        data = request.json
        new_todo = {"id": next_id, "task": data["task"], "completed": data.get("completed", False)}
        todos.append(new_todo)
        next_id += 1
        return new_todo, 201


@ns.route("/<int:id>")
@ns.response(404, "Todo not found")
@ns.param("id", "The task identifier")
class Todo(Resource):
    """Show a single task item and lets you delete them."""

    @ns.doc("get_todo")
    @ns.marshal_with(todo_model)
    def get(self, id):
        """Fetch a given resource."""
        todo = next((item for item in todos if item["id"] == id), None)
        if todo:
            return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    @ns.doc("delete_todo")
    @ns.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier."""
        global todos
        todos = [item for item in todos if item["id"] != id]
        return "", 204

    @ns.expect(todo_parser)
    @ns.marshal_with(todo_model)
    def put(self, id):
        """Update a task given its identifier."""
        data = request.json
        todo = next((item for item in todos if item["id"] == id), None)
        if not todo:
            api.abort(404, "Todo {} doesn't exist".format(id))
        todo["task"] = data.get("task", todo["task"])
        todo["completed"] = data.get("completed", todo["completed"])
        return todo
