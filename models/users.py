"""Класс User и функции работы с коллекцией пользователей."""

from typing import Optional


class User:
    """Пользователь системы."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f'{self.name} ({self.email})'

    @classmethod
    def from_data(cls, data: dict) -> 'User':
        """Создать пользователя из набора данных."""
        return cls(
            user_id=data['id'],
            name=data['name'],
            email=data['email'],
        )


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать объект User и добавить его в коллекцию."""
    if not users:
        user_id = 1
    else:
        user_id = max(user.id for user in users) + 1
    user = User(user_id, name, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке имени или email."""
    return [
        user for user in users
        if query.lower() in user.name.lower()
        or query.lower() in user.email.lower()
    ]


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print('Список пользователей пуст.')
        return
    print('--- Пользователи ---')
    for user in users:
        print(f'  id={user.id}: {user}')
