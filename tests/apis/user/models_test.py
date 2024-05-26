from mjv_todo_api.apis.user.models import User


def test_create_user(new_user: User) -> None:
    assert new_user.username == "testuser"
    assert new_user.email == "testuser@example.com"


def test_verify_password(new_user: User) -> None:
    assert new_user.verify_password("password")
    assert not new_user.verify_password("wrongpassword")


def test_change_password(new_user: User) -> None:
    new_password = "newpassword123"
    current_password = "password"
    new_user.change_password(current_password, new_password)
    assert not new_user.verify_password(current_password)
    assert new_user.verify_password(new_password)


def test_update_user(new_user: User) -> None:
    new_email = "newemail@example.com"
    new_password = "newpassword123"
    new_user.update(email=new_email, password=new_password)
    assert new_user.email == new_email
    assert new_user.verify_password(new_password)


def test_user_str_repr(new_user: User) -> None:
    assert str(new_user) == new_user.username
    assert repr(new_user) == f"<User '{new_user.username}'>"
