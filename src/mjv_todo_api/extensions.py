"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api(version="1.0", title="To-Do API", description="A simple To-Do API")
bcrypt = Bcrypt()
jwt = JWTManager()
