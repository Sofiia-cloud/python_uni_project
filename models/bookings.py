"""Класс Booking и функции работы с коллекцией бронирований."""

from datetime import date
from typing import Optional

from .rooms import Room
from .users import User


class Booking:
    """Бронирование помещения."""

    def __init__(
        self,
        booking_id: int,
        room: Room,
        booking_date: str,
        user: User,
    ) -> None:
        """Создать объект бронирования."""
        self.id = booking_id
        self.room = room
        self.booking_date = booking_date
        self.user = user
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить бронирование."""
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление бронирования."""
        status = 'отменено' if self.is_cancelled else 'активно'
        return (
            f'{self.room.name} на {self.booking_date} — '
            f'{self.user.name} ({status})'
        )


def is_room_available(
    bookings: list[Booking], room_id: int, booking_date: date
) -> bool:
    """Проверить, свободна ли аудитория на дату."""
    for booking in bookings:
        if (
            booking.room.id == room_id
            and booking.booking_date == booking_date.isoformat()
            and not booking.is_cancelled
        ):
            return False
    return True


def create_booking(
    bookings: list[Booking],
    room: Room,
    booking_date: date,
    user: User,
) -> Optional[Booking]:
    """Создать бронирование, если аудитория свободна."""
    if not is_room_available(bookings, room.id, booking_date):
        return None
    if not bookings:
        booking_id = 1
    else:
        booking_id = max(booking.id for booking in bookings) + 1
    booking = Booking(booking_id, room, booking_date.isoformat(), user)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int) -> bool:
    """Найти бронирование по id и отменить его."""
    for booking in bookings:
        if booking.id == booking_id:
            booking.cancel()
            return True
    return False


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус помещения."""
    if is_available:
        return 'Помещение доступно для бронирования'
    return 'Помещение уже занято'


def show_bookings(bookings: list[Booking]) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print('Бронирований нет.')
        return
    print('--- Бронирования ---')
    for booking in bookings:
        print(f'  id={booking.id}: {booking}')
