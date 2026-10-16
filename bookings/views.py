from django.shortcuts import render

from db.database import get_connection


BOOKING_SELECT = '''
    SELECT bookings.id, bookings.booking_date, bookings.is_cancelled,
           rooms.id AS room_id, rooms.name AS room_name,
           users.id AS user_id, users.name AS user_name,
           users.email AS user_email
    FROM bookings
    JOIN rooms ON bookings.room_id = rooms.id
    JOIN users ON bookings.user_id = users.id
'''


def bookings(request):
    with get_connection() as connection:
        bookings_list = connection.execute(
            BOOKING_SELECT
            + ' ORDER BY bookings.booking_date DESC, bookings.id DESC'
        ).fetchall()
    return render(
        request,
        'bookings/booking_list.html',
        {'bookings': bookings_list},
    )


def booking_detail(request, booking_id):
    with get_connection() as connection:
        booking = connection.execute(
            BOOKING_SELECT + ' WHERE bookings.id = ?', (booking_id,)
        ).fetchone()
    return render(
        request,
        'bookings/booking_detail.html',
        {'booking': booking},
        status=404 if booking is None else 200,
    )


def statistics(request):
    """Show active booking counts grouped by room."""
    with get_connection() as connection:
        statistics_data = connection.execute(
            '''SELECT rooms.id AS room_id, rooms.name AS room_name,
                      COUNT(bookings.id) AS bookings_count
               FROM rooms
               LEFT JOIN bookings
                 ON rooms.id = bookings.room_id AND bookings.is_cancelled = 0
               GROUP BY rooms.id, rooms.name
               ORDER BY bookings_count DESC, rooms.name'''
        ).fetchall()
    return render(
        request,
        'bookings/statistics.html',
        {'statistics': statistics_data},
    )
