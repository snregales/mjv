"""Todo's namespace POST parsers."""

from flask_restx.reqparse import RequestParser


def _todo_parser() -> RequestParser:
    parser = RequestParser()
    parser.add_argument("task", type=str, required=True, help="Task details", location="json")
    parser.add_argument("completed", type=bool, help="Task completion status", location="json")
    return parser


todo_parser: RequestParser = _todo_parser()
