import pytest
from sqlalchemy.orm.session import Session

from mjv.database import PkModel

# Did not go any deeper in testing database like checking unhappy paths like:
# id not found
# update non-existing field
# updating without commiting
# query data entries
# Since these are testing sqlalchemy's Model class and not my code


@pytest.fixture
def create_model[T: PkModel](session: Session, pk_model: type[T]) -> tuple[type[T], T]:  # type: ignore
    """Populate database with an entry."""
    instance = pk_model.create(name="Test Name")
    session.commit()
    return pk_model, instance


def test_pk_model_get_by_id[T: PkModel](create_model: tuple[type[T], T]) -> None:  # type: ignore
    model, instance = create_model
    assert instance == model.query.get_or_404(instance.id)


def test_update_model[T: PkModel](create_model: tuple[type[T], T]) -> None:  # type: ignore
    model, instance = create_model
    change = "Updated name"
    assert instance.name != change
    instance.update(name=change)
    instance = model.query.get(instance.id)
    assert instance
    assert instance.name == change


def test_delete_model[T: PkModel](create_model: tuple[type[T], T]) -> None:  # type: ignore
    model, instance = create_model
    instance.delete()
    assert not model.query.get(instance.id)


def test_field_descriptions[T: PkModel](pk_model: type[T]) -> None:  # type: ignore
    spec = dict(pk_model.field_descriptions())
    assert "id" in spec
    assert "created_at" in spec
    assert "modified_at" in spec
