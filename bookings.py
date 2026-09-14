"""Функции для работы с бронированиями."""

from datetime import date


def is_room_available(
    bookings: list[dict], room_id: int, booking_date: date
) -> bool:
    """Проверить, свободна ли аудитория на указанную дату."""
    for booking in bookings:
        if (
            booking['room_id'] == room_id
            and booking['date'] == booking_date.isoformat()
        ):
            return False
    return True


def create_booking(
    bookings: list[dict], room_id: int, booking_date: date
) -> dict | None:
    """Создать бронирование, если аудитория свободна."""
    if not is_room_available(bookings, room_id, booking_date):
        return None
    if not bookings:
        booking_id = 1
    else:
        booking_id = max(b['id'] for b in bookings) + 1
    new_booking = {
        'id': booking_id,
        'room_id': room_id,
        'date': booking_date.isoformat(),
    }
    bookings.append(new_booking)
    return new_booking


def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    """Отменить бронирование по идентификатору."""
    for booking in bookings:
        if booking['id'] == booking_id:
            bookings.remove(booking)
            return True
    return False


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус помещения."""
    if is_available:
        return 'Помещение доступно для бронирования'
    return 'Помещение уже занято'