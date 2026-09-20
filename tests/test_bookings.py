"""Тесты функций бронирования."""

from datetime import date

from bookings import (
    cancel_booking,
    create_booking,
    is_room_available,
)


def test_is_room_available():
    bookings = []
    assert is_room_available(bookings, 1, date(2026, 9, 15))


def test_duplicate_booking_forbidden():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 15), user_id=1)
    assert not is_room_available(bookings, 1, date(2026, 9, 15))


def test_cancelled_booking_does_not_block():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 15), user_id=1)
    cancel_booking(bookings, 1)
    assert is_room_available(bookings, 1, date(2026, 9, 15))
