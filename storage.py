"""Сохранение и загрузка объектов в JSON-файлах."""

import json
import os

from models import Booking, Room, User
from models.rooms import find_room_by_id
from models.users import find_user_by_id


def load_rooms(filename: str) -> list[Room]:
    """Загрузить аудитории из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [
            Room(item['id'], item['name'], item['capacity'])
            for item in data
        ]
    except (json.JSONDecodeError, ValueError, KeyError):
        print(f'Ошибка чтения файла {filename}. Данные проигнорированы.')
        return []


def save_rooms(filename: str, rooms: list[Room]) -> None:
    """Сохранить аудитории в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {'id': room.id, 'name': room.name, 'capacity': room.capacity}
        for room in rooms
    ]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [User.from_data(item) for item in data]
    except (json.JSONDecodeError, ValueError, KeyError):
        print(f'Ошибка чтения файла {filename}. Данные проигнорированы.')
        return []


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {'id': user.id, 'name': user.name, 'email': user.email}
        for user in users
    ]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_bookings(
    filename: str,
    rooms: list[Room],
    users: list[User],
) -> list[Booking]:
    """Загрузить бронирования и восстановить связи с Room и User."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, ValueError):
        print(f'Ошибка чтения файла {filename}. Данные проигнорированы.')
        return []

    bookings = []
    for item in data:
        room = find_room_by_id(rooms, item['room_id'])
        user = find_user_by_id(users, item['user_id'])
        if room is None or user is None:
            continue
        booking = Booking(
            booking_id=item['id'],
            room=room,
            booking_date=item['booking_date'],
            user=user,
        )
        booking.is_cancelled = item.get('is_cancelled', False)
        bookings.append(booking)
    return bookings


def save_bookings(filename: str, bookings: list[Booking]) -> None:
    """Сохранить бронирования в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {
            'id': booking.id,
            'room_id': booking.room.id,
            'booking_date': booking.booking_date,
            'user_id': booking.user.id,
            'is_cancelled': booking.is_cancelled,
        }
        for booking in bookings
    ]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
