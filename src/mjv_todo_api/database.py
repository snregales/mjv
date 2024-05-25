"""Database module, including the SQLAlchemy database object and DB-related utilities."""

from datetime import datetime
from typing import Any, Self, TypeAlias

import sqlalchemy
from flask_restx import Model as APIModel
from flask_restx import Namespace, OrderedModel

from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship
DataBasePrimitives: TypeAlias = bool | int | float | bytes | str | datetime


class CRUDMixin:
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs: DataBasePrimitives) -> Self:
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit: bool = True, **kwargs: DataBasePrimitives) -> Self:
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit: bool = True) -> Self:
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            db.session.commit()


class Model(CRUDMixin, db.Model):  # type: ignore [name-defined]
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods.

    Plus adds a 'primary key' column named ``id``.
    """

    __abstract__ = True
    id = Column(db.Integer, primary_key=True)

    @classmethod
    def rest_specification(cls, namespace: Namespace) -> APIModel | OrderedModel:
        """REST Swagger Specification."""
        raise NotImplementedError

    @classmethod
    def get_by_id(cls, record_id: str | bytes | int | float) -> Self | None:  # type: ignore
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.session.get(cls, int(record_id))  # type: ignore


def reference_col(
    tablename: str,
    nullable: bool = False,
    pk_name: str = "id",
    foreign_key_kwargs: dict[str, Any] | None = None,
    column_kwargs: dict[str, Any] | None = None,
) -> sqlalchemy.Column[Any]:
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(  # type: ignore
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
