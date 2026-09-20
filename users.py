"""Функции для работы с пользователями."""

from typing import Optional


def add_user(
    users: dict[int, dict],
    name: str,
    email: str,
) -> None:
    """Добавить пользователя в словарь users."""
    if not users:
        user_id = 1
    else:
        user_id = max(users.keys()) + 1
    users[user_id] = {'name': name, 'email': email}
    print(f'Пользователь "{name}" добавлен (id={user_id}).')


def find_user(
    users: dict[int, dict],
    query: str,
) -> dict[int, dict]:
    """Найти пользователей по подстроке имени или email."""
    found = {}
    for user_id, data in users.items():
        if (
            query.lower() in data['name'].lower()
            or query.lower() in data['email'].lower()
        ):
            found[user_id] = data
    return found


def find_user_by_id(
    users: dict[int, dict],
    user_id: int,
) -> Optional[dict]:
    """Найти пользователя по идентификатору."""
    return users.get(user_id)


def show_users(users: dict[int, dict]) -> None:
    """Вывести список пользователей."""
    if not users:
        print('Список пользователей пуст.')
        return
    print('--- Пользователи ---')
    for user_id, data in users.items():
        print(f'  id={user_id}: {data["name"]} ({data["email"]})')
