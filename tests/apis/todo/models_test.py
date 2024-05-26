from flask_sqlalchemy.session import Session

from mjv_todo_api.apis.todo.models import Todo
from mjv_todo_api.database import PkModel


# No need to create more CRUD tests, thats already done
# Just test that model inherits the CRUD Abstract class
def test_model_is_child_of_PkModel() -> None:
    assert issubclass(Todo, PkModel)


def test_update_todo_model(session: Session) -> None:
    todo = Todo.create(task="Initial Task")
    session.commit()
    todo.update(task="Updated Task", completed=True)
    session.commit()
    updated_todo = Todo.query.get(todo.id)
    assert updated_todo
    assert updated_todo.task == "Updated Task"
    assert updated_todo.completed is True
    assert updated_todo.completed_at is not None


def test_create_todo_model(session: Session) -> None:
    todo = Todo.create(task="Test Task")
    session.commit()
    assert todo.id
    assert todo.task == "Test Task"
    assert todo.completed is False
    assert todo.created_at is not None
    assert todo.modified_at is not None
    assert todo.completed_at is None


def test_field_descriptions() -> None:
    spec = dict(Todo.field_descriptions())
    assert "task" in spec
    assert "completed" in spec
    assert "completed_at" in spec
