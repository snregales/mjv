import pytest

from mjv.apis.todo.models import Todo
from mjv.apis.user.models import User
from mjv.database import PkModel


# No need to create more CRUD tests, thats already done
# Just test that model inherits the CRUD Abstract class
def test_model_is_child_of_PkModel() -> None:
    assert issubclass(Todo, PkModel)


@pytest.fixture(scope="module")
def new_todo(new_user: User) -> Todo:
    return Todo.create(task="Test Task", user_id=new_user.id)


def test_create_todo_model(new_todo: Todo) -> None:
    assert new_todo.task == "Test Task"
    assert new_todo.completed is False
    assert new_todo.completed_at is None


def test_update_todo_model(new_todo: Todo) -> None:
    new_todo.update(task="Updated Task", completed=True)
    updated_todo = Todo.query.get(new_todo.id)
    assert updated_todo
    assert updated_todo.task == "Updated Task"
    assert updated_todo.completed is True
    assert updated_todo.completed_at is not None


def test_field_descriptions() -> None:
    spec = dict(Todo.field_descriptions())
    assert "task" in spec
    assert "completed" in spec
    assert "completed_at" in spec
