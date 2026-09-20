"""Функции для работы с аудиториями."""


def add_room(rooms: dict[int, dict], room_name: str, capacity: int) -> None:
    """Добавить аудиторию в словарь rooms."""
    if not rooms:
        room_id = 1
    else:
        room_id = max(rooms.keys()) + 1
    rooms[room_id] = {'name': room_name, 'capacity': capacity}
    print(f'Аудитория "{room_name}" добавлена (id={room_id}).')


def find_room(rooms: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти аудитории по подстроке названия (без учёта регистра)."""
    found = {}
    for room_id, data in rooms.items():
        if query.lower() in data['name'].lower():
            found[room_id] = data
    return found


def find_room_by_id(rooms: dict[int, dict], room_id: int) -> dict | None:
    """Найти аудиторию по идентификатору."""
    return rooms.get(room_id)


def check_room_capacity(
    rooms: dict[int, dict], room_id: int, min_capacity: int
) -> bool:
    """Проверить, вмещает ли аудитория min_capacity человек."""
    if room_id not in rooms:
        return False
    return rooms[room_id]['capacity'] >= min_capacity


def filter_rooms_by_capacity(
    rooms: dict[int, dict], min_capacity: int
) -> dict[int, dict]:
    """Отобрать аудитории вместимостью не меньше min_capacity."""
    return {
        room_id: data
        for room_id, data in rooms.items()
        if data['capacity'] >= min_capacity
    }


def sort_rooms(rooms: dict[int, dict]) -> list[tuple[int, dict]]:
    """Вернуть аудитории, отсортированные по вместимости (по убыванию)."""
    return sorted(
        rooms.items(),
        key=lambda item: item[1]['capacity'],
        reverse=True,
    )


def show_rooms(rooms: dict[int, dict]) -> None:
    """Вывести список аудиторий."""
    if not rooms:
        print('Список аудиторий пуст.')
        return
    print('--- Аудитории ---')
    for room_id, data in rooms.items():
        print(f'  id={room_id}: {data["name"]} (до {data["capacity"]} чел.)')
