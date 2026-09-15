"""Тесты функций работы с аудиториями."""

from rooms import add_room, check_room_capacity, find_room, sort_rooms


def test_add_room():
    rooms = {}
    add_room(rooms, 'Аудитория 301', 30)
    assert len(rooms) == 1


def test_find_room():
    rooms = {}
    add_room(rooms, 'Аудитория 301', 30)
    assert find_room(rooms, 'аудитория')


def test_check_room_capacity():
    rooms = {}
    add_room(rooms, 'Конференц-зал', 60)
    assert check_room_capacity(rooms, 1, 50)


def test_sort_rooms():
    rooms = {}
    add_room(rooms, 'Малая', 10)
    add_room(rooms, 'Большая', 100)
    sorted_rooms = sort_rooms(rooms)
    assert sorted_rooms[0][1]['capacity'] == 100
