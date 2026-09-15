"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os


def load_rooms(filename: str) -> dict[int, dict]:
    """Загрузить аудитории из JSON-файла."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return {int(key): value for key, value in data.items()}
    except (json.JSONDecodeError, ValueError):
        print(f'Ошибка чтения файла {filename}. Данные проигнорированы.')
        return {}


def save_rooms(filename: str, rooms: dict[int, dict]) -> None:
    """Сохранить аудитории в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(rooms, file, ensure_ascii=False, indent=2)


def load_bookings(filename: str) -> list[dict]:
    """Загрузить бронирования из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, ValueError):
        print(f'Ошибка чтения файла {filename}. Данные проигнорированы.')
        return []


def save_bookings(filename: str, bookings: list[dict]) -> None:
    """Сохранить бронирования в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(bookings, file, ensure_ascii=False, indent=2)
