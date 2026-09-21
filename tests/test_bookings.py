"""Тесты класса Booking и функций бронирования."""

from datetime import date

from models import Booking, Room, User
from models.bookings import (
    cancel_booking,
    create_booking,
    is_room_available,
)


def make_room():
    return Room(1, 'Аудитория 301', 30)


def make_user():
    return User(1, 'Иван Петров', 'ivan@example.com')


def test_booking_creation():
    room = make_room()
    user = make_user()
    booking = Booking(1, room, '2026-09-15', user)
    assert booking.id == 1
    assert booking.room is room
    assert booking.user is user
    assert booking.booking_date == '2026-09-15'
    assert booking.is_cancelled is False


def test_booking_cancel():
    room = make_room()
    user = make_user()
    booking = Booking(1, room, '2026-09-15', user)
    booking.cancel()
    assert booking.is_cancelled is True


def test_is_room_available():
    bookings = []
    assert is_room_available(bookings, 1, date(2026, 9, 15))


def test_duplicate_booking_forbidden():
    room = make_room()
    user = make_user()
    bookings = []
    create_booking(bookings, room, date(2026, 9, 15), user)
    assert not is_room_available(bookings, room.id, date(2026, 9, 15))


def test_cancelled_booking_does_not_block():
    room = make_room()
    user = make_user()
    bookings = []
    create_booking(bookings, room, date(2026, 9, 15), user)
    cancel_booking(bookings, 1)
    assert is_room_available(bookings, room.id, date(2026, 9, 15))
