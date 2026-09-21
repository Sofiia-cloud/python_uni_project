"""Тесты класса User и функций работы с пользователями."""

from models import User
from models.users import add_user, find_user


def test_user_creation():
    user = User(1, 'Иван Петров', 'ivan@example.com')
    assert user.id == 1
    assert user.name == 'Иван Петров'
    assert user.email == 'ivan@example.com'


def test_user_from_data():
    user = User.from_data({
        'id': 1,
        'name': 'Иван Петров',
        'email': 'ivan@example.com',
    })
    assert user.id == 1
    assert user.name == 'Иван Петров'


def test_add_user():
    users = []
    add_user(users, 'Иван Петров', 'ivan@example.com')
    assert len(users) == 1


def test_find_user_by_name():
    users = []
    add_user(users, 'Иван Петров', 'ivan@example.com')
    assert find_user(users, 'Иван')


def test_find_user_by_email():
    users = []
    add_user(users, 'Иван Петров', 'ivan@example.com')
    assert find_user(users, 'ivan@example.com')
