"""Todo related models."""

from datetime import UTC, datetime
from typing import Self, override

from flask_restx import Model, Namespace, OrderedModel, fields

from mjv_todo_api.database import DataBasePrimitives, PkModel
from mjv_todo_api.extensions import db


class Todo(PkModel):
    """Todo ORM model."""

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    modified_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    completed_at = db.Column(db.DateTime)

    @override
    @classmethod
    def rest_specification(cls, namespace: Namespace) -> Model | OrderedModel:
        """REST Swagger Specification."""
        return namespace.model(
            cls.__name__,
            {
                "id": fields.Integer(readOnly=True, description="The unique identifier of a task"),
                "task": fields.String(required=True, description="The task details"),
                "completed": fields.Boolean(description="Task completion status"),
                "created_at": fields.DateTime(readOnly=True, description="The creation timestamp"),
                "modified_at": fields.DateTime(
                    readOnly=True, description="The last modified timestamp"
                ),
                "completed_at": fields.DateTime(description="The completion timestamp"),
            },
        )

    @override
    def update(self, commit: bool = True, **kwargs: DataBasePrimitives) -> Self:
        """Update specific fields of todo."""
        if "completed" in kwargs and kwargs["completed"]:
            kwargs.setdefault("completed_at", datetime.now(UTC))
        return super().update(commit, **kwargs)
