"""Точка запуска приложения «Сервис поиска свободных аудиторий»."""

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
    show_rooms,
    sort_rooms,
)
from storage import (
    load_bookings,
    load_rooms,
    load_users,
    save_bookings,
    save_rooms,
    save_users,
)
from users import add_user, find_user, show_users
from utils import input_date, input_int

ROOMS_FILE = 'data/rooms.json'
USERS_FILE = 'data/users.json'
BOOKINGS_FILE = 'data/bookings.json'


def show_bookings(
    bookings: list[dict],
    rooms: dict[int, dict],
    users: dict[int, dict],
) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print('Бронирований нет.')
        return
    print('--- Бронирования ---')
    for booking in bookings:
        room = rooms.get(booking['room_id'], {'name': '?'})
        user = users.get(booking['user_id'], {'name': '?'})
        status = 'отменено' if booking.get('is_cancelled', False) else 'активн'
        print(
            f'  id={booking["id"]}: {room["name"]} '
            f'на {booking["date"]} — {user["name"]} ({status})'
        )


def create_new_booking(
    bookings: list[dict],
    rooms: dict[int, dict],
    users: dict[int, dict],
) -> None:
    """Сценарий создания бронирования."""
    room_id = input_int('id аудитории: ')
    if room_id not in rooms:
        print('Аудитория не найдена.')
        return
    user_id = input_int('id пользователя: ')
    if user_id not in users:
        print('Пользователь не найден.')
        return
    booking_date = input_date('Дата (ДД.ММ.ГГГГ): ')
    created = create_booking(bookings, room_id, booking_date, user_id)
    if created:
        save_bookings(BOOKINGS_FILE, bookings)
        print(f'Бронирование создано (id={created["id"]}).')
    else:
        print('Не удалось создать бронирование: помещение занято.')


def main() -> None:
    """Точка запуска: меню приложения."""
    rooms = load_rooms(ROOMS_FILE)
    users = load_users(USERS_FILE)
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
        print('9. Показать пользователей')
        print('10. Добавить пользователя')
        print('11. Найти пользователя')
        print('12. Добавить аудиторию')
        print('13. Отобрать аудитории по вместимости')
        print('0. Выход')

        choice = input_int('Выберите действие: ')

        if choice == 1:
            show_rooms(rooms)
        elif choice == 2:
            query = input('Подстрока названия: ')
            show_rooms(find_room(rooms, query))
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
            create_new_booking(bookings, rooms, users)
        elif choice == 6:
            booking_id = input_int('id бронирования: ')
            if cancel_booking(bookings, booking_id):
                save_bookings(BOOKINGS_FILE, bookings)
                print('Бронирование отменено.')
            else:
                print('Бронирование не найдено.')
        elif choice == 7:
            show_bookings(bookings, rooms, users)
        elif choice == 8:
            for room_id, data in sort_rooms(rooms):
                print(f'  id={room_id}: {data["name"]} ({data["capacity"]})')
        elif choice == 9:
            show_users(users)
        elif choice == 10:
            name = input('Имя пользователя: ')
            email = input('Email: ')
            add_user(users, name, email)
            save_users(USERS_FILE, users)
        elif choice == 11:
            query = input('Подстрока имени или email: ')
            show_users(find_user(users, query))
        elif choice == 12:
            name = input('Название аудитории: ')
            capacity = input_int('Вместимость: ')
            add_room(rooms, name, capacity)
            save_rooms(ROOMS_FILE, rooms)
        elif choice == 13:
            min_capacity = input_int('Минимальная вместимость: ')
            show_rooms(filter_rooms_by_capacity(rooms, min_capacity))
        elif choice == 0:
            save_rooms(ROOMS_FILE, rooms)
            save_users(USERS_FILE, users)
            save_bookings(BOOKINGS_FILE, bookings)
            print('Данные сохранены. До встречи!')
            break
        else:
            print('Неизвестная команда.')


if __name__ == '__main__':
    main()
