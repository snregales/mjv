"""User's namespace POST Parsers."""

from flask_restx.reqparse import RequestParser


def _register_parser() -> RequestParser:
    parser = RequestParser()
    parser.add_argument("username", type=str, required=True, help="Username is required")
    parser.add_argument("email", type=str, required=True, help="Email is required")
    parser.add_argument("password", type=str, required=True, help="Password is required")
    return parser


def _login_parser() -> RequestParser:
    parser = RequestParser()
    parser.add_argument("username", type=str, required=True, help="Username is required")
    parser.add_argument("password", type=str, required=True, help="Password is required")
    return parser


def _password_change_parser() -> RequestParser:
    parser = RequestParser()
    parser.add_argument("old_password", type=str, required=True, help="Old password is required")
    parser.add_argument("new_password", type=str, required=True, help="New password is required")
    return parser


register_parser: RequestParser = _register_parser()
login_parser: RequestParser = _login_parser()
password_parser: RequestParser = _password_change_parser()
