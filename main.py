"""Точка запуска приложения «Сервис поиска свободных аудиторий»."""

from datetime import date

from bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_room_available,
)
from rooms import (
    add_room,
    check_room_capacity,
    filter_rooms_by_capacity,
    find_room,
    sort_rooms,
)
from storage import load_bookings, load_rooms, save_bookings, save_rooms
from utils import input_date, input_int

ROOMS_FILE = 'data/rooms.json'
BOOKINGS_FILE = 'data/bookings.json'


def show_rooms(rooms: dict[int, dict]) -> None:
    """Вывести список аудиторий."""
    if not rooms:
        print('Список аудиторий пуст.')
        return
    print('--- Аудитории ---')
    for room_id, data in rooms.items():
        print(f'  id={room_id}: {data["name"]} (до {data["capacity"]} чел.)')


def show_bookings(bookings: list[dict], rooms: dict[int, dict]) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print('Бронирований нет.')
        return
    print('--- Бронирования ---')
    for booking in bookings:
        room = rooms.get(booking['room_id'], {'name': '?'})
        print(
            f'  id={booking["id"]}: {room["name"]} '
            f'на {booking["date"]}'
        )


def main() -> None:
    """Точка запуска: меню приложения."""
    rooms = load_rooms(ROOMS_FILE)
    bookings = load_bookings(BOOKINGS_FILE)

    while True:
        print()
        print('=== Сервис поиска свободных аудиторий ===')
        print('1. Показать аудитории')
        print('2. Найти аудиторию по названию')
        print('3. Проверить вместимость')
        print('4. Проверить доступность на дату')
        print('5. Забронировать аудиторию')
        print('6. Отменить бронирование')
        print('7. Показать бронирования')
        print('8. Отсортировать аудитории по вместимости')
        print('0. Выход')

        choice = input_int('Выберите действие: ')

        if choice == 1:
            show_rooms(rooms)
        elif choice == 2:
            query = input('Подстрока названия: ')
            found = find_room(rooms, query)
            show_rooms(found)
        elif choice == 3:
            room_id = input_int('id аудитории: ')
            min_capacity = input_int('Минимальная вместимость: ')
            ok = check_room_capacity(rooms, room_id, min_capacity)
            print('Подходит' if ok else 'Не подходит')
        elif choice == 4:
            room_id = input_int('id аудитории: ')
            booking_date = input_date('Дата (ДД.ММ.ГГГГ): ')
            available = is_room_available(bookings, room_id, booking_date)
            print(get_booking_status(available))
        elif choice == 5:
            room_id = input_int('id аудитории: ')
            booking_date = input_date('Дата (ДД.ММ.ГГГГ): ')
            created = create_booking(bookings, room_id, booking_date)
            if created:
                save_bookings(BOOKINGS_FILE, bookings)
                print(f'Бронирование создано (id={created["id"]}).')
            else:
                print('Не удалось создать бронирование: помещение занято.')
        elif choice == 6:
            booking_id = input_int('id бронирования: ')
            if cancel_booking(bookings, booking_id):
                save_bookings(BOOKINGS_FILE, bookings)
                print('Бронирование отменено.')
            else:
                print('Бронирование не найдено.')
        elif choice == 7:
            show_bookings(bookings, rooms)
        elif choice == 8:
            for room_id, data in sort_rooms(rooms):
                print(f'  id={room_id}: {data["name"]} ({data["capacity"]})')
        elif choice == 0:
            save_rooms(ROOMS_FILE, rooms)
            save_bookings(BOOKINGS_FILE, bookings)
            print('Данные сохранены. До встречи!')
            break
        else:
            print('Неизвестная команда.')


if __name__ == '__main__':
    main()