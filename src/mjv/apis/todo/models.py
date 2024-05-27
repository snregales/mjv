"""Todo related models."""

from datetime import UTC, datetime
from typing import Any, Iterable, Self, override

from flask_restx.fields import Boolean, DateTime, Integer, String

from mjv.database import Column, DataBasePrimitives, PkModel, reference_col
from mjv.extensions import db


class Todo(PkModel):
    """Todo ORM model."""

    task = Column(db.String(80), nullable=False)
    completed = Column(db.Boolean, default=False)
    completed_at = Column(db.DateTime)
    user_id = reference_col("user", nullable=False)
    user = db.relationship("User", back_populates="todos")

    def __str__(self) -> str:
        """User instance string representation."""
        return f"{self.id}: {self.task}"

    def __repr__(self) -> str:
        """User instance representation."""
        return f"<{self.__class__.__name__} '{self}'>"

    @override
    @classmethod
    def field_descriptions(cls) -> Iterable[tuple[str, Any]]:
        """Todo fields metadata."""
        return (
            ("task", String(required=True, description="The task details")),
            ("completed", Boolean(description="Task completion status")),
            ("completed_at", DateTime(description="The completion timestamp")),
            (
                "user_id",
                Integer(readOnly=True, description="The ID of the user who owns the task"),
            ),
            *super().field_descriptions(),
        )

    @override
    def update(self, commit: bool = True, **kwargs: DataBasePrimitives) -> Self:
        """Update specific todo fields."""
        if "completed" in kwargs and kwargs["completed"]:
            kwargs.setdefault("completed_at", datetime.now(UTC))
        return super().update(commit, **kwargs)
