"""Тесты функций работы с пользователями."""

from users import add_user, find_user


def test_add_user():
    users = {}
    add_user(users, 'Иван Петров', 'ivan@example.com')
    assert len(users) == 1


def test_find_user_by_name():
    users = {}
    add_user(users, 'Иван Петров', 'ivan@example.com')
    assert find_user(users, 'Иван')


def test_find_user_by_email():
    users = {}
    add_user(users, 'Иван Петров', 'ivan@example.com')
    assert find_user(users, 'ivan@example.com')
