"""User routes."""

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from flask_restx._http import HTTPStatus
from flask_restx.fields import String

from .models import User
from .parsers import login_parser, password_parser, register_parser

ns = Namespace("auth", description="Authentication operations")

user_model = ns.model(
    "User",
    {
        key: value
        for key, value in User.field_descriptions()
        if key in ("id", "username", "email", "password")
    },
)


@ns.route("/register")
class Register(Resource):
    """User registration operations."""

    @ns.expect(register_parser)
    @ns.marshal_with(user_model, code=HTTPStatus.CREATED)
    def post(self) -> tuple[User, HTTPStatus]:
        """Create a new user."""
        args = register_parser.parse_args()
        username = args.get("username")
        email = args.get("email")

        if (
            User.query.filter_by(username=username).first()
            or User.query.filter_by(email=email).first()
        ):
            ns.abort(HTTPStatus.BAD_REQUEST, "User already exists")

        return User.create(**args), HTTPStatus.CREATED


@ns.route("/login")
class Login(Resource):
    """User login operations."""

    @ns.expect(login_parser)
    @ns.marshal_with(
        ns.model(
            "AccessToken",
            {"access_token": String(required=True, description="The JWT access token")},
        ),
        code=HTTPStatus.OK,
    )
    def post(self) -> tuple[dict[str, str], HTTPStatus]:
        """Usere login."""
        args = login_parser.parse_args()
        username = args.get("username")
        user = User.query.filter_by(username=username).first()

        if user is None or not user.verify_password(args.get("password")):
            ns.abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials")

        return {"access_token": create_access_token(identity=user.id)}, HTTPStatus.OK


@ns.route("/current_user")
class CurrentUser(Resource):
    """Current user operations."""

    @jwt_required()
    @ns.marshal_with(user_model, code=HTTPStatus.OK)
    def get(self) -> tuple[User, HTTPStatus]:
        """Get current user."""
        return User.query.get(get_jwt_identity()), HTTPStatus.OK

    @jwt_required()
    @ns.expect(password_parser)
    @ns.marshal_with(user_model, code=HTTPStatus.OK)
    def put(self) -> tuple[User, HTTPStatus]:
        """Change user password."""
        return User.query.get(get_jwt_identity()).change_password(
            **password_parser.parse_args()
        ), HTTPStatus.OK
