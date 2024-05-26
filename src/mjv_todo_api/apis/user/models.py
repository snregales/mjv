"""User models."""

from typing import Any, Iterable, Self, override

from flask_restx.fields import String

from mjv_todo_api.database import Column, DataBasePrimitives, PkModel
from mjv_todo_api.extensions import bcrypt, db


def _encrypt_password(
    password: str | None, **kwargs: DataBasePrimitives
) -> dict[str, DataBasePrimitives]:
    if password:
        kwargs["password"] = bcrypt.generate_password_hash(password).decode("utf-8")
    return kwargs


class User(PkModel):
    """User ORM model."""

    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(120), unique=True, nullable=False)
    password = Column(db.String(128), nullable=False)

    def __str__(self) -> str:
        """User instance string representation."""
        return str(self.username)

    def __repr__(self) -> str:
        """User instance representation."""
        return f"<{self.__class__.__name__} '{self.username}'>"

    def verify_password(self, password: str) -> bool:
        """Verify that the given password matches the users."""
        return bcrypt.check_password_hash(self.password, password)  # type: ignore

    def change_password(self, old_password: str, new_password: str) -> Self | None:  # type: ignore
        """Change password if old_password is verified."""
        if self.verify_password(old_password):
            return self.update(password=new_password)

    @override
    @classmethod
    def field_descriptions(cls) -> Iterable[tuple[str, Any]]:
        """User fields metadata."""
        return (
            ("username", String(required=True, description="The username")),
            ("email", String(required=True, description="The email address")),
            ("password", String(required=True, description="The user password")),
            *super().field_descriptions(),
        )

    @override
    @classmethod
    def create(cls, **kwargs: DataBasePrimitives) -> Self:
        """Create a new user and save it the database."""
        return super().create(**_encrypt_password(**kwargs))  # type: ignore

    @override
    def update(self, commit: bool = True, **kwargs: DataBasePrimitives) -> Self:
        """Update specific user fields."""
        return super().update(commit, **_encrypt_password(**kwargs))  # type: ignore
