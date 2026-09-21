"""Класс Room и функции работы с коллекцией аудиторий."""

from typing import Optional


class Room:
    """Помещение для бронирования."""

    def __init__(self, room_id: int, name: str, capacity: int) -> None:
        """Создать объект помещения."""
        self.id = room_id
        self.name = name
        self.capacity = capacity

    def is_suitable_for(self, people_count: int) -> bool:
        """Проверить, подходит ли помещение по вместимости."""
        return self.capacity >= people_count

    def __str__(self) -> str:
        """Вернуть строковое представление помещения."""
        return f'{self.name}, {self.capacity} мест'


def add_room(rooms: list[Room], name: str, capacity: int) -> Room:
    """Создать объект Room и добавить его в коллекцию."""
    if not rooms:
        room_id = 1
    else:
        room_id = max(room.id for room in rooms) + 1
    room = Room(room_id, name, capacity)
    rooms.append(room)
    return room


def find_room(rooms: list[Room], query: str) -> list[Room]:
    """Найти аудитории по подстроке названия."""
    return [room for room in rooms if query.lower() in room.name.lower()]


def find_room_by_id(rooms: list[Room], room_id: int) -> Optional[Room]:
    """Найти аудиторию по идентификатору."""
    for room in rooms:
        if room.id == room_id:
            return room
    return None


def check_room_capacity(
    rooms: list[Room], room_id: int, min_capacity: int
) -> bool:
    """Проверить вместимость аудитории по её id."""
    room = find_room_by_id(rooms, room_id)
    if room is None:
        return False
    return room.is_suitable_for(min_capacity)


def filter_rooms_by_capacity(
    rooms: list[Room], min_capacity: int
) -> list[Room]:
    """Отобрать аудитории по вместимости."""
    return [room for room in rooms if room.capacity >= min_capacity]


def sort_rooms(rooms: list[Room]) -> list[Room]:
    """Отсортировать аудитории по вместимости (по убыванию)."""
    return sorted(rooms, key=lambda room: room.capacity, reverse=True)


def show_rooms(rooms: list[Room]) -> None:
    """Вывести список аудиторий."""
    if not rooms:
        print('Список аудиторий пуст.')
        return
    print('--- Аудитории ---')
    for room in rooms:
        print(f'  id={room.id}: {room}')
